"""Exercise real installs and updates against a disposable local Git remote."""

import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = "scripts/sync-playbook.py"
LOCK = ".agents/playbook-lock.json"


class SyncTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.source = self.base / "upstream"
        self.source.mkdir()
        for name in ("skills", "templates", "scripts"):
            shutil.copytree(ROOT / name, self.source / name)
        shutil.copy2(ROOT / "playbook.json", self.source / "playbook.json")
        self.git("init", "--quiet")
        self.git("config", "user.name", "Playbook Test")
        self.git("config", "user.email", "playbook@example.invalid")
        self.commit()
        self.target = self.base / "xyz"
        self.target.mkdir()

    def git(self, *args):
        result = subprocess.run(
            ["git", "-C", str(self.source), *args], capture_output=True, text=True, check=True
        )
        return result.stdout.strip()

    def commit(self):
        self.git("add", ".")
        self.git("commit", "--quiet", "-m", "Fixture revision")
        return self.git("rev-parse", "HEAD")

    def run_sync(self, *args, installed=False, expected=0):
        script = (self.target if installed else ROOT) / SCRIPT
        result = subprocess.run(
            [sys.executable, str(script), *args], cwd=self.base,
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result

    def install(self, *args):
        return self.run_sync("--target", str(self.target), "--source", str(self.source), *args)

    def snapshot(self):
        return {p.relative_to(self.target).as_posix(): p.read_bytes()
                for p in self.target.rglob("*") if p.is_file()}

    def test_install_is_self_contained_and_preserves_project_instructions(self):
        custom = b"# XYZ\r\n\r\nUse pnpm. Keep the existing stack.\r\n"
        (self.target / "AGENTS.md").write_bytes(custom)
        self.install()
        self.assertTrue((self.target / "AGENTS.md").read_bytes().startswith(custom))
        self.assertFalse(any(p.is_symlink() for p in self.target.rglob("*")))
        lock = json.loads((self.target / LOCK).read_text())
        self.assertEqual(lock["revision"], self.git("rev-parse", "HEAD"))
        self.assertFalse(lock["source_dirty"])
        self.assertEqual(len(lock["skills"]), 3)
        self.assertTrue((self.target / ".agents/templates/feature-spec.md").is_file())
        self.assertTrue((self.target / ".agents/templates/lab.md").is_file())
        # Removing upstream still leaves skill content and all bundled templates readable.
        shutil.rmtree(self.source)
        for name in lock["skills"]:
            skill = self.target / ".agents/skills" / name / "SKILL.md"
            self.assertTrue(skill.is_file())
            import re
            for reference in re.findall(r"`(\.\./\.\./templates/[^`]+)`", skill.read_text()):
                self.assertTrue((skill.parent / reference).is_file(), reference)

    def test_all_standalone_skills_include_nested_resources(self):
        names = list(json.loads((ROOT / "playbook.json").read_text())["skills"])
        self.install("--skills", *names)
        self.assertTrue((self.target / ".agents/skills/production-readiness/references/release-checks.md").is_file())
        self.assertFalse((self.target / "_bmad").exists())
        self.assertFalse((self.target / "product-draft").exists())

    def test_git_line_ending_conversion_is_not_a_local_conflict(self):
        self.install()
        for file in self.target.rglob("*"):
            if file.is_file():
                file.write_bytes(file.read_bytes().replace(b"\n", b"\r\n"))
        before = self.snapshot()
        self.run_sync("--check", installed=True)
        self.assertEqual(before, self.snapshot())
        source_skill = self.source / "skills/learn-before-build/SKILL.md"
        source_skill.write_text(source_skill.read_text() + "\nUpdated guidance\n")
        self.commit()
        self.run_sync("--update", installed=True)
        self.assertIn(b"Updated guidance", (self.target / ".agents/skills/learn-before-build/SKILL.md").read_bytes())

    def test_check_update_and_repeat_from_installed_script(self):
        self.install()
        original = self.snapshot()
        self.run_sync("--check", installed=True)
        self.assertEqual(original, self.snapshot())
        source_skill = self.source / "skills/learn-before-build/SKILL.md"
        source_skill.write_text(source_skill.read_text() + "\nNew upstream guidance.\n")
        # Update the updater too; it is copied, never executed from the fetched source.
        updater = self.source / SCRIPT
        updater.write_text(updater.read_text() + "\n# New updater revision\n")
        instructions = self.source / "templates/consumer-agents.md"
        instructions.write_text(instructions.read_text() + "\nNew managed guidance.\n")
        revision = self.commit()
        self.run_sync("--check", installed=True, expected=1)
        self.assertEqual(original, self.snapshot())
        agents = self.target / "AGENTS.md"
        agents.write_bytes(b"# Custom prefix\n" + agents.read_bytes() + b"\nCustom suffix\n")
        self.run_sync("--update", installed=True)
        self.assertIn(b"New upstream guidance", (self.target / ".agents/skills/learn-before-build/SKILL.md").read_bytes())
        self.assertTrue(agents.read_bytes().startswith(b"# Custom prefix\n"))
        self.assertTrue(agents.read_bytes().endswith(b"\nCustom suffix\n"))
        self.assertIn(b"New managed guidance.", agents.read_bytes())
        self.assertEqual(json.loads((self.target / LOCK).read_text())["revision"], revision)
        updated = self.snapshot()
        self.run_sync("--update", installed=True)
        self.assertEqual(updated, self.snapshot())

    def test_local_edits_deletions_and_managed_instructions_block_all_writes(self):
        self.install()
        file = self.target / ".agents/skills/learn-before-build/SKILL.md"
        clean = file.read_bytes()
        file.write_bytes(clean + b"\nLocal change\n")
        original = self.snapshot()
        self.run_sync("--update", installed=True, expected=2)
        self.assertEqual(original, self.snapshot())
        file.unlink()
        original = self.snapshot()
        self.run_sync("--update", installed=True, expected=2)
        self.assertEqual(original, self.snapshot())
        file.write_bytes(clean)
        agents = self.target / "AGENTS.md"
        agents.write_bytes(agents.read_bytes().replace(b"## Engineering playbook", b"## Local policy"))
        original = self.snapshot()
        self.run_sync("--check", installed=True, expected=2)
        self.assertEqual(original, self.snapshot())

    def test_unmanaged_collisions_unknown_skills_and_symlinks_do_not_write(self):
        file = self.target / ".agents/skills/learn-before-build/SKILL.md"
        file.parent.mkdir(parents=True)
        file.write_text("Existing skill")
        original = self.snapshot()
        self.install_error("--skills", "learn-before-build")
        self.assertEqual(original, self.snapshot())
        self.install_error("--skills", "bmad-spec-workflow")
        self.assertEqual(original, self.snapshot())
        shutil.rmtree(self.target / ".agents")
        external = self.base / "external"
        external.mkdir()
        (self.target / ".agents").symlink_to(external, target_is_directory=True)
        self.install_error()
        self.assertEqual(list(external.iterdir()), [])

    def install_error(self, *args):
        return self.run_sync("--target", str(self.target), "--source", str(self.source), *args, expected=2)

    def test_selection_change_prunes_only_unchanged_managed_files(self):
        self.install()
        extra = self.target / ".agents/skills/learn-before-build/local-notes.md"
        extra.write_text("Keep my notes")
        self.run_sync("--update", "--skills", "production-readiness", installed=True)
        self.assertEqual(extra.read_text(), "Keep my notes")
        self.assertFalse((extra.parent / "SKILL.md").exists())
        self.assertFalse((self.target / ".agents/templates/feature-spec.md").exists())
        agents = (self.target / "AGENTS.md").read_text()
        self.assertIn("production-readiness/SKILL.md", agents)
        self.assertNotIn("learn-before-build/SKILL.md", agents)

    def test_explicit_commit_and_network_failure_preserve_target(self):
        first = self.git("rev-parse", "HEAD")
        self.install()
        template = self.source / "templates/learning-record.md"
        template.write_text(template.read_text() + "\nUpstream template change\n")
        self.commit()
        self.run_sync("--update", "--ref", first, installed=True)
        self.assertEqual(json.loads((self.target / LOCK).read_text())["revision"], first)
        original = self.snapshot()
        self.run_sync("--update", "--source", str(self.base / "absent"), installed=True, expected=2)
        self.assertEqual(original, self.snapshot())

    def test_non_default_branch_and_template_updates(self):
        self.install()
        default = self.git("branch", "--show-current")
        self.git("checkout", "--quiet", "-b", "preview")
        template = self.source / "templates/learning-record.md"
        template.write_text(template.read_text() + "\nPreview learning template\n")
        preview = self.commit()
        self.git("checkout", "--quiet", default)
        self.run_sync("--update", "--ref", "preview", installed=True)
        self.assertEqual(json.loads((self.target / LOCK).read_text())["revision"], preview)
        self.assertIn("Preview learning template", (self.target / ".agents/templates/learning-record.md").read_text())

    def test_source_and_target_guards(self):
        self.run_sync(expected=2)
        self.run_sync("--target", str(ROOT), expected=2)
        self.run_sync("--target", str(self.target), "--check", expected=2)
        self.install()
        before = self.snapshot()
        self.run_sync(installed=True, expected=2)
        self.run_sync("--update", "--ref", "absent-reference", installed=True, expected=2)
        self.assertEqual(before, self.snapshot())

    def test_parent_file_collision_and_update_collision_do_not_write(self):
        (self.target / "scripts").write_text("An existing project file")
        before = self.snapshot()
        self.install_error()
        self.assertEqual(before, self.snapshot())
        (self.target / "scripts").unlink()
        self.install()
        new_file = "skills/learn-before-build/references/new.md"
        upstream = self.source / new_file
        upstream.parent.mkdir()
        upstream.write_text("Upstream resource")
        self.commit()
        local = self.target / (".agents/" + new_file)
        local.parent.mkdir()
        local.write_text("My local resource")
        before = self.snapshot()
        self.run_sync("--update", installed=True, expected=2)
        self.assertEqual(before, self.snapshot())

    def test_bad_markers_and_lock_path_traversal_do_not_write(self):
        self.install()
        agents = self.target / "AGENTS.md"
        original_agents = agents.read_bytes()
        agents.write_bytes(original_agents + b"<!-- engineering-playbook:begin -->")
        original = self.snapshot()
        self.run_sync("--update", installed=True, expected=2)
        self.assertEqual(original, self.snapshot())
        agents.write_bytes(original_agents)
        lock_file = self.target / LOCK
        lock = json.loads(lock_file.read_text())
        lock["files"]["../../outside"] = "0" * 64
        lock_file.write_text(json.dumps(lock))
        original = self.snapshot()
        self.run_sync("--update", installed=True, expected=2)
        self.assertEqual(original, self.snapshot())

    def test_write_failure_restores_previous_files(self):
        spec = importlib.util.spec_from_file_location("sync_playbook", ROOT / SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        (self.target / "AGENTS.md").write_text("Keep this")
        original_write = module.atomic_write
        calls = []

        def fail_once(path, data):
            calls.append(path)
            if len(calls) == 2:
                raise OSError("Simulated write failure")
            original_write(path, data)

        original = self.snapshot()
        with patch.object(module, "atomic_write", side_effect=fail_once):
            with self.assertRaises(OSError):
                module.apply(self.target, {"AGENTS.md": b"Changed", "new.txt": b"New"})
        self.assertEqual(original, self.snapshot())


if __name__ == "__main__":
    unittest.main()
