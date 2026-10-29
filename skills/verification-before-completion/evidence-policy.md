# Valid evidence policy — local A0/A18 profile

This is the shared evidence contract for the local Superpowers skills.
Reading this reference does not activate an additional workflow.

## Select reuse or verification

1. Name the claim and its acceptance requirements, including any method the
   user explicitly requires. Find the existing result that actually supports it:
   source/log or operation ID, command/action, exit or terminal result, coverage,
   and the relevant code/artifact/configuration/environment/input state.
2. Reuse that result when it covers this claim and those relevant conditions
   are unchanged. A new agent, phase transition, handoff, or completion message
   does not invalidate it. Read the result; do not run a summary command that
   silently repeats tests or hashes.
3. Reverify only when a relevant condition changed or a specific unanswered
   doubt exists. Start with the affected behavior. Expand to a full suite when
   cross-module risk, unresolved impact, or an explicit project/user requirement
   justifies that coverage; keep mandatory host checks in force.
4. Report the actual result and its limits. A failed, missing, or invalidated
   result cannot prove success. Only the affected claims become unverified;
   unrelated valid evidence remains usable.

Use existing plans, ledgers, logs, and receipts. Do not create a new evidence
framework, recurring hash loop, or independent review layer to establish reuse.
Known changes, existing revision records and receipts can establish identity;
do necessary integrity checks when identity is genuinely uncertain.
An unsupported concern that some unrelated file might change is not a concrete
evidence gap. Preserving one artifact does not authorize a hash baseline of
read-only notes, prompts, scripts or the entire project.

A historical snapshot proves its recorded state. Live service health, new
external operations, or changing data may require new evidence because the
underlying state changed, not because a new message is being written.

## Completion and specified methods

Report outcome acceptance and required-method acceptance separately.
A typed query, screenshot, or alternative write path does not prove a required
typed write. For a critical unverified method, test the smallest authorized
object/copy before large production work. Preserve successful artifacts and
prefer a copy for additional proof; disclose partial completion honestly.
Only the user may change or waive an explicitly required method or acceptance
boundary. A coordinator may route the evidence and recommend a disposition;
its advice does not itself change the requirement.

## Existing task-done protocol

Choose one completion path, not two successive copies of the same check:

- When a necessary check has not been recorded, run the appropriate final
  GREEN/check through `bash scripts/task-done PLAN N BASE --acceptance TARGET -- COMMAND ...`.
  It records the command's actual result in the existing log and ledger.
- When the same task already has valid successful evidence, cite that record.
  If invoking the helper again, use
  `bash scripts/task-done PLAN N BASE --reuse --acceptance TARGET -- COMMAND ...`. This mode checks the saved
  success/ledger against BASE, HEAD and a clean Git worktree, and does not
  execute a test or append another completion line.
- Reuse mode covers only a successful run recorded by this helper on an
  unchanged clean Git snapshot. The caller must separately assess environment,
  configuration, external inputs and acceptance requirements. Dirty snapshots,
  old logs without the success footer, changed code, or failed checks are not
  automatically reusable through this mode. Do not label them as passing.

Reuse must bind the current task and plan, the exact expected command/arguments, and the current acceptance target. V2 task-done requires those inputs on reuse and rejects mismatches; legacy unbound logs cannot be reused by the helper. A known reachable defect, a failing result, or an unmet explicit verification/method requirement invalidates the affected claim even when Git is unchanged. The helper checks identity only; never invoke reuse as a substitute for that missing check. For external environment/config/input changes, assess their relevance and verify the affected behavior.
