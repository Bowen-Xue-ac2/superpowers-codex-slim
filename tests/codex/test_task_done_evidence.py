"""Exercise successful evidence reuse and stale/failed evidence rejection."""
from pathlib import Path
import os
import shutil
import stat
import subprocess
import tempfile
import unittest


PLUGIN = Path(__file__).resolve().parents[2]
BASH = Path(r"C:\Program Files\Git\bin\bash.exe")
TASK_DONE = PLUGIN / "skills/executing-plans/scripts/task-done"


class TaskEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp_parent = Path(tempfile.gettempdir()).resolve()
        self.temp = Path(tempfile.mkdtemp(prefix="sp-task-evidence-")).resolve()
        self.repo = self.temp / "repo"
        self.repo.mkdir()
        self.env = dict(os.environ, GIT_CONFIG_GLOBAL=os.devnull,
                        GIT_CONFIG_NOSYSTEM="1")
        self.git("init", "-q")
        self.git("config", "user.name", "Fixture")
        self.git("config", "user.email", "fixture@example.invalid")
        self.git("config", "commit.gpgsign", "false")
        self.git("config", "core.autocrlf", "false")
        (self.repo / "plan.md").write_text("# Plan\n\n## Task 1: Fixture\n", encoding="utf-8")
        (self.repo / "source.txt").write_text("original\n", encoding="utf-8")
        self.git("add", ".")
        self.git("commit", "-qm", "fixture")
        self.base = self.git("rev-parse", "HEAD").strip()
        self.workspace = self.repo / ".superpowers/sdd/plan"
        self.command = ["sh", "-c", "printf x >> .superpowers/sdd/plan/invocations; printf '3 tests passed\\n'"]

    def tearDown(self):
        target = self.temp.resolve()
        assert target != self.temp_parent
        assert target.is_relative_to(self.temp_parent)
        assert target.name.startswith("sp-task-evidence-")
        def clear_readonly(func, path, exc):
            assert Path(path).resolve().is_relative_to(target)
            os.chmod(path, stat.S_IREAD | stat.S_IWRITE)
            func(path)
        shutil.rmtree(target, onexc=clear_readonly)

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.repo, env=self.env,
                              text=True, encoding="utf-8", capture_output=True,
                              check=True, timeout=15).stdout

    def done(self, *args, target="fixture tests", command=None, task="1", plan="plan.md"):
        if args == ("--reuse",):
            args = ("--reuse", "--acceptance", target, "--", *(command or self.command))
        elif args and args[0] == "--":
            args = ("--acceptance", target, *args)
        return subprocess.run([str(BASH), TASK_DONE.as_posix(), plan, task, self.base, *args],
                              cwd=self.repo, env=self.env, text=True, encoding="utf-8",
                              capture_output=True, timeout=15)

    def success(self):
        result = self.done("--", *self.command)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result

    def test_successful_reuse_does_not_execute_again_or_duplicate_completion(self):
        self.success()
        ledger = self.workspace / "progress.md"
        before = ledger.read_bytes()
        result = self.done("--reuse")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.workspace / "invocations").read_text(), "x")
        self.assertEqual(ledger.read_bytes(), before)

    def test_missing_evidence_cannot_create_completion(self):
        self.assertNotEqual(self.done("--reuse").returncode, 0)
        self.assertFalse((self.workspace / "progress.md").exists())

    def test_failed_command_is_not_reusable_or_recorded_as_complete(self):
        result = self.done("--", "sh", "-c", "echo failed; exit 7")
        self.assertEqual(result.returncode, 7, result.stderr)
        self.assertNotEqual(self.done("--reuse").returncode, 0)
        ledger = self.workspace / "progress.md"
        self.assertTrue(not ledger.exists() or "complete" not in ledger.read_text(encoding="utf-8"))

    def test_changed_commit_invalidates_evidence(self):
        self.success()
        (self.repo / "source.txt").write_text("changed\n", encoding="utf-8")
        self.git("add", "source.txt")
        self.git("commit", "-qm", "changed")
        self.assertNotEqual(self.done("--reuse").returncode, 0)

    def test_dirty_worktree_invalidates_evidence(self):
        self.success()
        (self.repo / "source.txt").write_text("uncommitted\n", encoding="utf-8")
        self.assertNotEqual(self.done("--reuse").returncode, 0)

    def test_replaced_log_without_success_record_is_not_reusable(self):
        self.success()
        (self.workspace / "task-1-tests.log").write_text("OK\n", encoding="utf-8")
        self.assertNotEqual(self.done("--reuse").returncode, 0)

    def test_success_with_empty_output_can_be_reused(self):
        result = self.done("--", "true")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.done("--reuse", command=["true"]).returncode, 0)

    def test_changed_command_arguments_rejected(self):
        self.success()
        self.assertNotEqual(self.done("--reuse", command=["true"]).returncode, 0)

    def test_changed_acceptance_rejected(self):
        self.success()
        self.assertNotEqual(self.done("--reuse", target="required full suite").returncode, 0)

    def test_changed_plan_even_if_ignored_rejected(self):
        self.success()
        self.git("update-index", "--assume-unchanged", "plan.md")
        (self.repo / "plan.md").write_text("# Different acceptance\n", encoding="utf-8")
        self.assertNotEqual(self.done("--reuse").returncode, 0)

    def test_different_task_rejected(self):
        self.success()
        self.assertNotEqual(self.done("--reuse", task="2").returncode, 0)

    def test_legacy_or_unbound_reuse_is_rejected(self):
        self.success()
        result = subprocess.run([str(BASH), TASK_DONE.as_posix(), "plan.md", "1", self.base, "--reuse"], cwd=self.repo, env=self.env, capture_output=True)
        self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
