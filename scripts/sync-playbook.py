#!/usr/bin/env python3
"""Vendor selected engineering skills; update only unchanged managed files.

Python 3.9+ and Git are the only dependencies. No downloaded code is executed.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile


SOURCE_URL = "https://github.com/pandey-g/engineering-playbook.git"
LOCK = ".agents/playbook-lock.json"
SCRIPT = "scripts/sync-playbook.py"
BEGIN = b"<!-- engineering-playbook:begin -->"
END = b"<!-- engineering-playbook:end -->"
NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")


class SyncError(Exception):
    pass


def canonical(data):
    """Ignore Git's LF/CRLF conversion for UTF-8 text, preserving binary bytes."""
    if data is None or b"\0" in data:
        return data
    try:
        data.decode("utf-8")
    except UnicodeDecodeError:
        return data
    return data.replace(b"\r\n", b"\n")


def digest(data):
    return hashlib.sha256(canonical(data)).hexdigest()


def git(root, *args):
    result = subprocess.run(
        ["git", "-C", str(root), *args], capture_output=True, text=True, timeout=120
    )
    if result.returncode:
        raise SyncError(result.stderr.strip() or "Git command failed")
    return result.stdout.strip()


def safe_path(root, relative):
    """Reject traversal and symlinked destinations, including parent folders."""
    parts = PurePosixPath(relative).parts
    if not parts or PurePosixPath(relative).is_absolute() or any(
        part in ("..", ".") for part in parts
    ) or "\\" in relative or str(PurePosixPath(relative)) != relative:
        raise SyncError("Invalid relative path: " + relative)
    path = root
    for index, part in enumerate(parts):
        path = path / part
        if path.is_symlink():
            raise SyncError("Symlink is not a managed file or directory: " + str(path))
        if index < len(parts) - 1 and path.exists() and not path.is_dir():
            raise SyncError("Expected a directory: " + str(path))
    return path


def managed_path(relative):
    parts = PurePosixPath(relative).parts
    return relative == SCRIPT or (
        len(parts) >= 4 and parts[:2] == (".agents", "skills")
        and NAME.fullmatch(parts[2]) is not None
    ) or (len(parts) >= 3 and parts[:2] == (".agents", "templates"))


def read_optional(path):
    if path.exists() and not path.is_file():
        raise SyncError("Expected a regular file: " + str(path))
    return path.read_bytes() if path.exists() else None


def load_lock(target):
    raw = read_optional(safe_path(target, LOCK))
    if raw is None:
        return None
    lock = json.loads(raw)
    if not isinstance(lock, dict) or lock.get("schema") != 1 or not isinstance(lock.get("files"), dict):
        raise SyncError("Unsupported or invalid playbook lock file")
    for path, checksum in lock["files"].items():
        safe_path(target, path)
        if not managed_path(path) or not re.fullmatch(r"[0-9a-f]{64}", checksum):
            raise SyncError("Invalid managed file in lock: " + path)
    if not re.fullmatch(r"[0-9a-f]{64}", lock.get("agents_block_sha256", "")):
        raise SyncError("Invalid AGENTS.md checksum in lock")
    return lock


def split_agents(data):
    if data.count(BEGIN) != 1 or data.count(END) != 1:
        raise SyncError("AGENTS.md managed markers are missing or ambiguous")
    start = data.index(BEGIN)
    finish = data.index(END) + len(END)
    if finish <= start:
        raise SyncError("AGENTS.md managed markers are out of order")
    return data[:start], data[start:finish], data[finish:]


def bundle(source, selected):
    manifest = json.loads(safe_path(source, "playbook.json").read_text())
    if not isinstance(manifest, dict) or manifest.get("schema") != 1:
        raise SyncError("Unsupported source manifest")
    selected = sorted(set(selected or manifest["default_skills"]))
    payload = {}
    for name in selected:
        if not NAME.fullmatch(name) or name not in manifest["skills"]:
            raise SyncError("Unsupported skill: " + name + ". BMAD requires separate setup.")
        folder = safe_path(source, "skills/" + name)
        if not (folder / "SKILL.md").is_file():
            raise SyncError("Missing SKILL.md for " + name)
        for path in sorted(folder.rglob("*")):
            relative = path.relative_to(source).as_posix()
            safe_path(source, relative)
            if path.is_file():
                payload[".agents/" + relative] = path.read_bytes()
        for template in manifest["skills"][name]["templates"]:
            path = safe_path(source, "templates/" + template)
            payload[".agents/templates/" + template] = path.read_bytes()
    payload[SCRIPT] = safe_path(source, SCRIPT).read_bytes()
    for path in payload:
        if not managed_path(path):
            raise SyncError("Source manifest produced invalid destination: " + path)
    routes = "\n".join(
        "- `{0}`: `.agents/skills/{0}/SKILL.md`".format(name) for name in selected
    )
    instructions = safe_path(source, "templates/consumer-agents.md").read_text()
    block = BEGIN + b"\n" + instructions.format(skill_routes=routes).encode() + END
    return selected, payload, block


def plan(target, old, payload, block):
    """Check every conflict before making any target changes."""
    changes = {}
    conflicts = []
    previous = old["files"] if old else {}
    for relative in sorted(set(previous) | set(payload)):
        current = read_optional(safe_path(target, relative))
        if relative in previous:
            if current is None or digest(current) != previous[relative]:
                conflicts.append(relative + " (managed file edited or deleted)")
        elif current is not None:
            conflicts.append(relative + " (existing unmanaged file)")
        wanted = payload.get(relative)
        if canonical(current) != canonical(wanted):
            changes[relative] = wanted
    current = read_optional(safe_path(target, "AGENTS.md"))
    if old:
        prefix, existing, suffix = split_agents(current or b"")
        if digest(existing) != old["agents_block_sha256"]:
            conflicts.append("AGENTS.md (managed section edited)")
        wanted = prefix + block + suffix
    else:
        current = current or b""
        if BEGIN in current or END in current:
            raise SyncError("AGENTS.md already has playbook markers but no lock file")
        separator = b"" if not current or current.endswith(b"\n\n") else (
            b"\n" if current.endswith(b"\n") else b"\n\n"
        )
        wanted = current + separator + block + b"\n"
    if canonical(current) != canonical(wanted):
        changes["AGENTS.md"] = wanted
    if conflicts:
        raise SyncError("No files changed. Resolve local conflicts first:\n  " + "\n  ".join(conflicts))
    return changes


def atomic_write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    mode = path.stat().st_mode & 0o777 if path.exists() else 0o644
    descriptor, name = tempfile.mkstemp(prefix=".playbook-", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
        os.chmod(name, mode)
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def apply(target, changes):
    originals = {}
    try:
        for relative, data in changes.items():
            path = safe_path(target, relative)
            originals[relative] = read_optional(path)
            if data is None:
                path.unlink()
            else:
                atomic_write(path, data)
    except OSError:
        for relative, data in reversed(list(originals.items())):
            path = safe_path(target, relative)
            if data is None:
                path.unlink(missing_ok=True)
            else:
                atomic_write(path, data)
        raise


def sync(args, source, target, old, source_url):
    if source == target:
        raise SyncError("Choose a consuming repository, not the playbook checkout itself")
    selected, payload, block = bundle(source, args.skills or (old["skills"] if old else None))
    revision = git(source, "rev-parse", "HEAD")
    dirty = bool(git(source, "status", "--porcelain", "--untracked-files=all"))
    new = {
        "schema": 1,
        "source": source_url,
        "revision": revision,
        "source_dirty": dirty,
        "skills": selected,
        "files": {name: digest(data) for name, data in sorted(payload.items())},
        "agents_block_sha256": digest(block),
    }
    changes = plan(target, old, payload, block)
    lock_data = (json.dumps(new, indent=2, sort_keys=True) + "\n").encode()
    if canonical(read_optional(safe_path(target, LOCK))) != lock_data:
        changes[LOCK] = lock_data  # Write provenance last.
    print("Source commit: " + revision)
    if dirty:
        print("Source has uncommitted files; hashes record the installed copy.")
    if not changes:
        print("Playbook is up to date.")
        return 0
    for name, data in changes.items():
        print(("REMOVE " if data is None else "WRITE  ") + name)
    if args.check:
        print("Updates available; target files were not changed.")
        return 1
    apply(target, changes)
    print("Playbook installed. Review git diff, then commit the managed files.")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path, help="Consumer root; installed script defaults to its own repo")
    parser.add_argument("--skills", nargs="+", help="Complete desired skill selection")
    parser.add_argument("--source", help="Git URL or local Git checkout to fetch updates from")
    parser.add_argument("--ref", help="Source branch, tag or commit; default is source default branch HEAD")
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--check", action="store_true", help="Read-only check; exit 1 if updates exist")
    action.add_argument("--update", action="store_true", help="Apply upstream updates")
    args = parser.parse_args(argv)
    script_root = Path(__file__).resolve().parent.parent
    target = (args.target or script_root).expanduser().resolve()
    try:
        if not target.is_dir():
            raise SyncError("Target directory must already exist")
        old = load_lock(target)
        if old and not (args.check or args.update):
            raise SyncError("Already installed. Choose --check or --update.")
        if not old and (args.check or args.update):
            raise SyncError("No installation found. Install first using --target.")
        if not old and args.target is None:
            raise SyncError("Initial installation requires --target /path/to/xyz")
        if not old and args.source is None and args.ref is None:
            return sync(args, script_root, target, old, SOURCE_URL)
        source_url = args.source or (old["source"] if old else SOURCE_URL)
        if not isinstance(source_url, str) or source_url.startswith("-"):
            raise SyncError("Invalid Git source")
        # A local source is recorded as an absolute path; remote URLs remain portable.
        if Path(source_url).expanduser().exists():
            source_url = str(Path(source_url).expanduser().resolve())
        with tempfile.TemporaryDirectory(prefix="engineering-playbook-") as temporary:
            checkout = Path(temporary) / "source"
            print("Fetching playbook source...", flush=True)
            git(Path(temporary), "clone", "--quiet", "--no-checkout", "--", source_url, str(checkout))
            reference = args.ref or "HEAD"
            try:
                revision = git(checkout, "rev-parse", "--verify", "--end-of-options", reference + "^{commit}")
            except SyncError:
                # Clones create remote-tracking refs for non-default branches.
                revision = git(checkout, "rev-parse", "--verify", "--end-of-options", "refs/remotes/origin/" + reference + "^{commit}")
            git(checkout, "checkout", "--quiet", "--detach", revision)
            return sync(args, checkout, target, old, source_url)
    except (SyncError, OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired) as error:
        print("Error: " + str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
