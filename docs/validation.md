# Validation scope

Date: 2026-10-29. Platform: Windows, Codex CLI 0.165.0.

The matching pre-publication installation was checked through the host's native
skill registry and fresh CLI tasks. Observed criteria:

| Criterion | Observed behavior |
|---|---|
| Ordinary development | No SP skill read; required local tests ran |
| Explicit enable | The entry and requested debugging skill were read |
| Single-skill scope | No other named workflow was loaded |
| Same-state evidence | Existing actual results were inspected; zero test reruns |
| Relevant change | Only the affected test ran; its failure was reported honestly |

V2 task-done: 12 tests passed in disposable Git fixtures, covering successful
reuse, no duplicate completion record, failures/missing/corrupt evidence, changed
commit/worktree/plan, a different task, command or acceptance target, and rejection
of unbound reuse. Test source is in `tests/codex/test_task_done_evidence.py`.

The public snapshot preserves those skill/helper bytes. It changes package
metadata, documentation and public artifact selection. Prior results are reused
for their matching scope; no public-installation behavior run, Desktop reload,
real compaction event, cross-host guarantee or speed/token benchmark is claimed.

Raw receipts remain private because they contain workstation paths and session
metadata. This summary is not a fabricated replacement for raw execution output.
