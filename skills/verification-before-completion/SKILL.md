---
name: verification-before-completion
description: "Use only within the user's explicitly enabled Superpowers task and phase, or when the user explicitly requests this skill for supporting completion claims with valid evidence."
---

# Verification Before Completion — local A0/A18 profile

**Core principle:** Evidence before claims. Validity follows relevant state
and coverage, not the number of messages since a command ran.

The single evidence contract is [evidence-policy.md](evidence-policy.md).
Other local skills consume that same contract; they do not add a fresh-run
or full-suite gate merely because a new phase begins.

## Gate

Before a completion claim:

1. Identify the claim, its required result and any explicitly required method.
2. Read existing evidence and decide whether it remains valid under the shared
   contract. Cite its source, coverage and state when it does.
3. If a relevant state changed or a specific gap remains, run the smallest
   authorized check that answers it. Broaden coverage only for actual impact
   or an explicit project requirement.
4. Inspect the real result/exit or terminal status. Report completion, partial
   completion or blockage with the corresponding evidence.

## Evidence by claim

| Claim | Required evidence |
| --- | --- |
| Tests pass | Actual successful output for the relevant unchanged code and selected coverage |
| Build succeeds | Successful build result for the relevant state, not a linter result |
| Bug fixed | Regression/symptom evidence that covers the actual fix |
| Required method works | The specified operation really occurred; a query does not prove a write |
| Requirements met | Outcome and method acceptance each checked against the agreed scope |
| Agent completed | Inspect its actual changes and valid evidence; a success report alone is insufficient |
| External delivery complete | Original operation reached a terminal result and required target/path/version evidence is available |

A previous run is reusable when valid. Confidence, stale logs, a changed
artifact or a different acceptance criterion is not a substitute for evidence.
Read a garbled or truncated result at its existing source before concluding
that it is missing; do not regenerate it solely because it was hard to read.

## Partial results and external operations

Queued, pending and running states are not completed delivery. Follow the
original operation to a terminal outcome and verify the required target,
path and version. On unknown, reconcile the original ID and actual target
before deciding on a retry; never treat unknown as permission to resend.

Report unverified required methods or missing checks as gaps. Stopping a
workflow, reaching a budget, or omitting a full suite does not itself prove
the task passed. Preserve mandatory host checks and user approval boundaries.
