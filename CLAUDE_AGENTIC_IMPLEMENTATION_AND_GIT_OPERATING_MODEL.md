# Claude Agentic Implementation and Git Operating Model

Version: 1.0  
Status: controlled implementation companion for Release 0 and Release 1A delivery  
Primary purpose: define how Claude Code, specialized agents, Git branches, commits, pull requests, continuous integration, and implementation evidence are used to build the AI Trading Decision Platform safely and incrementally.

Canonical inputs:

```text
AI_TRADING_SYSTEM_CANONICAL_SPECIFICATION_V4.md
RELEASE_0_1A_IMPLEMENTATION_BACKLOG.md
RELEASE_0_TESTING_LOGIC_AND_ARCHITECTURE.md
REQUIREMENT_TO_CODE_COVERAGE_MATRIX.md
CANONICAL_SCHEMA_ADDENDUM_CONTENT_FEATURES.md
```

This document does not add product scope. It defines an implementation operating model for converting the canonical requirements into reviewed, tested, traceable code.

---

## 1. Authority and Conflict Resolution

The canonical specification remains the highest authority.

The authority order for implementation work is:

```text
1. AI_TRADING_SYSTEM_CANONICAL_SPECIFICATION_V4.md
2. RELEASE_0_1A_IMPLEMENTATION_BACKLOG.md
3. RELEASE_0_TESTING_LOGIC_AND_ARCHITECTURE.md
4. REQUIREMENT_TO_CODE_COVERAGE_MATRIX.md
5. CANONICAL_SCHEMA_ADDENDUM_CONTENT_FEATURES.md
6. This operating model
7. GitHub issue or task instructions
8. Agent-generated implementation plans
```

If a lower-level artifact conflicts with a higher-level artifact, the higher-level artifact wins.

An agent MUST NOT silently resolve a material conflict by inventing a requirement, threshold, schema field, risk rule, or production policy. It must record the conflict as `BLOCKED`, cite the affected requirement IDs, and identify the smallest human decision required.

Documentation coverage is not implementation evidence. Code existence is not test evidence. A successful test is not production promotion.

---

## 2. Operating Objective

The agentic delivery system exists to close implementation slices through reproducible evidence.

The target workflow is:

```text
canonical requirement
  -> implementation slice
  -> branch
  -> tests
  -> implementation
  -> independent review
  -> CI evidence
  -> pull request
  -> human merge decision
  -> coverage matrix update
```

The agentic system must optimize for:

```text
correctness
point-in-time safety
small reviewable changes
deterministic tests
traceability
reversibility
clear blocked-state reporting
```

It must not optimize for:

```text
maximum generated code
maximum number of simultaneous agents
advanced-model novelty
large unreviewed refactors
rapid expansion of product scope
automatic production promotion
```

---

## 3. Current Delivery Boundary

Until Release 0 closes, autonomous implementation work is restricted to the Release 0 truth chain:

```text
provider isolation
  -> canonical OHLCV normalization
  -> point-in-time labels for 5, 8, and 14 exchange sessions
  -> feature snapshot and training/latest schema parity
  -> deterministic checkpoint and resume
  -> purged walk-forward validation and embargo
  -> approved baseline model and reproducible report
  -> requirement-to-code coverage update
```

The following capabilities are outside the Release 0 autonomous critical path:

```text
FinBERT
news and social ingestion
LSTM, GRU, TCN, Transformer, or TFT models
knowledge graph or graph neural network
advanced macro and graph modules
counterfactual portfolios
LLM explanations
broker execution
paper trading
live trading
```

These capabilities may be inspected or documented, but they must not consume Release 0 closure effort unless a governance-approved scope change explicitly promotes them.

---

## 4. Repository Operating Model

### 4.1 Repository Meaning

The Git repository is the controlled home of:

```text
source code
tests
schemas
configuration
documentation
migration files
CI workflows
implementation history
review evidence
```

The repository has two synchronized forms:

```text
local repository: the working copy on a developer or agent runtime
remote repository: the shared GitHub repository
```

Git tracks history locally. GitHub coordinates shared branches, pull requests, reviews, CI status, issue tracking, and merge controls.

### 4.2 Recommended Repository Layout

```text
repository/
├── CLAUDE.md
├── .claude/
│   ├── agents/
│   ├── rules/
│   ├── skills/
│   └── settings.json
├── .github/
│   ├── workflows/
│   ├── ISSUE_TEMPLATE/
│   └── PULL_REQUEST_TEMPLATE.md
├── docs/
│   ├── AI_TRADING_SYSTEM_CANONICAL_SPECIFICATION_V4.md
│   ├── RELEASE_0_1A_IMPLEMENTATION_BACKLOG.md
│   ├── RELEASE_0_TESTING_LOGIC_AND_ARCHITECTURE.md
│   ├── REQUIREMENT_TO_CODE_COVERAGE_MATRIX.md
│   ├── CANONICAL_SCHEMA_ADDENDUM_CONTENT_FEATURES.md
│   ├── CLAUDE_AGENTIC_IMPLEMENTATION_AND_GIT_OPERATING_MODEL.md
│   └── AUTONOMOUS_RELEASE_0_REPORT.md
├── src/
│   ├── data/
│   ├── labels/
│   ├── features/
│   ├── validation/
│   ├── orchestration/
│   ├── models/
│   ├── reporting/
│   └── governance/
├── tests/
│   ├── fixtures/
│   └── release0/
├── scripts/
│   ├── validate_requirement_refs.py
│   ├── validate_coverage_matrix.py
│   ├── check_no_secrets.py
│   └── generate_release0_report.py
└── pyproject.toml
```

The actual layout may differ, but the boundaries between source, tests, documentation, governance scripts, and agent configuration must remain explicit.

---

## 5. Git Concepts and Their Role in Agentic Delivery

### 5.1 Branch

A branch is an isolated line of development.

Agents must never implement directly on `main`. Each coherent implementation slice uses its own branch.

Recommended branch names:

```text
r0/spec-reference-lint
r0/ohlcv-adapter
r0/pit-labels
r0/schema-parity
r0/checkpoint-replay
r0/purged-walk-forward
r0/baseline-model
r1a/recommendation-schema
r1a/runtime-manifest
```

A branch protects the stable codebase from incomplete or experimental work and allows multiple independent tasks to proceed without overwriting each other.

### 5.2 Commit

A commit is an immutable historical checkpoint containing a coherent change and a message explaining its purpose.

A commit should answer:

```text
what changed
why it changed
which requirement or task it supports
```

Recommended commit examples:

```text
test(r0): add canonical OHLCV MultiIndex contract fixtures
feat(r0): implement deterministic OHLCV normalization
fix(r0): reject duplicate canonical bar timestamps
docs(trace): record passing OHLCV test evidence
```

A commit must not combine unrelated changes such as an OHLCV adapter, LSTM experiment, documentation rewrite, and CI configuration.

### 5.3 Push

Push uploads local commits to the remote GitHub repository.

Agents may push only to their assigned feature branch. They must not push directly to `main`, rewrite shared branch history, or force-push unless a documented emergency recovery procedure permits it.

### 5.4 Pull Request

A pull request, or PR, is a reviewable proposal to merge one branch into another, normally a feature branch into `main`.

A PR is the required review boundary for agent-generated code. It contains:

```text
scope
requirement IDs
changed files
test commands
test results
review findings
known limitations
non-goals
coverage matrix changes
```

The PR is where CI, independent agents, and humans decide whether the proposed code is safe to merge.

### 5.5 Merge

Merge integrates the approved branch into `main`.

For this project, automatic merge is disabled by default. A human must approve merges involving:

```text
financial logic
point-in-time behavior
labels
validation
risk or portfolio policy
execution behavior
readiness thresholds
golden fixtures
canonical schemas
```

A merged branch becomes part of the shared project history and a dependency for later slices.

### 5.6 Conflict

A Git conflict occurs when two branches modify incompatible parts of the same content and Git cannot safely choose the correct result.

An agent must not resolve a semantic conflict by selecting one side blindly. It must compare both changes against the canonical requirements and rerun all affected tests.

---

## 6. Agent Topology

The recommended topology separates coordination, implementation, testing, temporal review, and evidence control.

```text
release-controller
│
├── requirements-auditor
├── code-archaeologist
│
├── current-slice
│   ├── test-designer
│   └── slice-implementer
│
├── pit-reviewer
└── integration-and-coverage-agent
```

Not every agent runs continuously. Agents are activated only when their responsibility is needed.

### 6.1 Release Controller

Purpose: control scope, dependencies, task selection, and final reporting.

Responsibilities:

```text
read backlog and coverage matrix
select the next dependency-safe slice
create or refine the GitHub issue
assign requirement IDs and acceptance criteria
create or authorize the feature branch
coordinate specialist agents
classify blockers
prevent advanced-scope drift
produce the autonomous run report
```

Forbidden behavior:

```text
large direct implementations
changing canonical requirements
changing readiness thresholds
merging into main
marking tests passed without evidence
```

### 6.2 Requirements Auditor

Purpose: validate that task references and companion documents remain consistent with the canonical specification.

Responsibilities:

```text
validate all REQ-* references
detect missing or invalid requirement IDs
identify semantic conflicts
check release criticality mappings
check authority order
maintain the requirement-reference validation script
```

The requirements auditor should run before implementation and in CI after documentation changes.

### 6.3 Code Archaeologist

Purpose: inspect existing code before new implementation is created.

Responsibilities:

```text
locate existing implementations
identify duplicated logic
map code to requirements
identify candidate modules for extraction
identify unsafe coupling
identify missing tests
recommend retain, refactor, deprecate, or replace decisions
```

The code archaeologist is read-only. It must not refactor while investigating.

### 6.4 Test Designer

Purpose: translate requirements and failure modes into executable tests.

Responsibilities:

```text
create contract tests
create golden fixtures
create PIT and maturity tests
create property-based tests where appropriate
create deterministic failure assertions
record test IDs
```

The test designer must not weaken existing tests, silently change expected outputs, or modify implementation merely to make a test pass.

### 6.5 Slice Implementer

Purpose: implement one bounded backlog slice.

Responsibilities:

```text
inspect the existing implementation plan
change only approved files
implement the smallest coherent solution
run targeted tests
run formatting and static analysis
create coherent commits
push to the assigned branch
prepare PR evidence
```

The implementer must not expand the task into adjacent backlog items.

### 6.6 PIT Reviewer

Purpose: independently review temporal correctness and leakage risk.

Responsibilities:

```text
review event and availability timestamps
review label maturity
review exchange-session alignment
review train, validation, and test boundaries
review transformation fit windows
review universe and sector membership timing
review checkpoint compatibility and replay context
review target leakage and forbidden columns
```

The PIT reviewer is read-only and must report findings as:

```text
BLOCKER
MAJOR
MINOR
OBSERVATION
```

Each finding must include file, line, requirement ID, failure explanation, and a reproduction test or deterministic verification method.

### 6.7 Integration and Coverage Agent

Purpose: verify the integrated slice and update implementation evidence.

Responsibilities:

```text
run the full Release 0 regression suite
run lint and type checks
run requirement-reference validation
run coverage-matrix validation
verify PR evidence
update code locations and test IDs
record latest test result
produce artifact hashes when required
```

This agent may update a row to `TESTED_RESEARCH` only after the required evidence exists.

---

## 7. Model Allocation Policy

Model assignment should reflect task complexity rather than using the strongest model for every operation.

Recommended policy:

| Agent or task | Model class | Reason |
| --- | --- | --- |
| Release controller | strongest long-context reasoning model | maintains architecture, dependencies, and multi-step state |
| Requirements auditor | balanced reasoning model; escalate ambiguous conflicts | mostly structured validation with occasional semantic analysis |
| Code archaeologist | fast or balanced coding model | search, mapping, and summarization |
| Test designer | balanced coding model | converts contracts into executable tests |
| Slice implementer | balanced coding model | routine implementation and refactoring |
| PIT reviewer | strongest reasoning model | independent high-risk temporal audit |
| Integration and coverage | fast or balanced model | deterministic commands and structured updates |

Escalation to a stronger model is appropriate when:

```text
requirements conflict
multiple modules require coordinated refactoring
PIT behavior is ambiguous
schema migration affects canonical entities
review findings disagree
```

Model choice must never replace deterministic tests or human approval.

---

## 8. Release 0 Execution Sequence

### 8.1 Stage 0: Specification and Repository Hygiene

Required outputs:

```text
all REQ-* references validated
invalid references corrected or blocked
CLAUDE.md created
agent definitions created
CI baseline created
tests/release0 directory created
code inventory produced
```

No financial implementation should begin until the authority and traceability chain is reliable.

### 8.2 Stage 1: Canonical OHLCV Adapter

Primary requirements:

```text
REQ-CONV-DATA-001 through REQ-CONV-DATA-006
```

Required test themes:

```text
flat single-instrument input
provider MultiIndex input
field-ticker and ticker-field layouts
one-dimensional numeric Series output
missing required field
non-numeric field
duplicate timestamp
unsorted timestamp
mixed timezone
header normalization
source lineage
stable output schema
```

Completion of this stage is required before label and feature work.

### 8.3 Stage 2: Point-in-Time Labels

Primary requirements:

```text
REQ-LAB-001 through REQ-LAB-013
```

Required test themes:

```text
5-session label
8-session label
14-session label
exchange-session counting
last rows remain NOT_MATURED
label_available_at
missing bars
split and corporate-action handling
delisting and terminal events
after-hours event behavior
price-basis declaration
```

### 8.4 Stage 3: Training and Latest Schema Parity

Primary requirements:

```text
REQ-CONV-DS-003 through REQ-CONV-DS-008
REQ-SCH-037
REQ-SCH-038
```

Required test themes:

```text
approved feature list is authoritative
same feature order
same numeric dtypes
no target columns in latest features
no future_* columns
no label_* columns
no actual_* columns
no pred_* columns
stable feature schema hash
registered missingness only
```

### 8.5 Stage 4: Checkpoint and Resume Determinism

Primary requirements:

```text
REQ-CONV-OVN-003 through REQ-CONV-OVN-010
```

Required test themes:

```text
configuration hash validation
code version validation
schema version validation
universe and trading-date validation
artifact checksum validation
idempotent retry
resume after multiple interruption points
uninterrupted and resumed artifact hashes match
incompatible checkpoint rejection
```

### 8.6 Stage 5: Purged Walk-Forward and Embargo

Primary requirements:

```text
REQ-VAL-001 through REQ-VAL-008
```

Required test themes:

```text
date-grouped folds
label-interval purge
embargo enforcement
no train/test overlap
empty-fold handling
minimum history
reproducible fold manifest
final-holdout isolation
```

### 8.7 Stage 6: Baseline Evidence

Primary requirements:

```text
REQ-MOD-001 through REQ-MOD-010
REQ-VAL-004 through REQ-VAL-010
```

The baseline runs only after all upstream gates pass.

A no-edge baseline result is a valid research outcome. The system must report `BLOCKED_NO_EDGE` or an equivalent status instead of changing thresholds, folds, labels, or expected results after observing performance.

---

## 9. Concurrency Policy

### 9.1 Default Rule

Work is sequential when one slice depends on the output contract of another.

Examples:

```text
labels wait for canonical OHLCV
schema parity waits for approved feature schema
baseline waits for PIT labels and purged validation
```

### 9.2 Allowed Parallelism

Parallel work is allowed only when tasks:

```text
have no unresolved dependency relationship
use separate branches or Git worktrees
do not edit the same files
do not redefine shared schemas
do not change the same fixtures
```

A safe Release 0 example after schema parity is complete:

```text
Agent A: checkpoint and resume
Agent B: purged walk-forward splitter
```

### 9.3 Forbidden Parallelism

```text
two agents push to the same branch
two agents edit the same canonical schema
multiple agents redesign the same adapter
implementation starts before tests and contracts are resolved
advanced-model agents consume Release 0 critical-path resources
```

---

## 10. Branch, Commit, and Pull Request Rules

### 10.1 One Slice per Branch

Each branch must contain one coherent backlog slice.

### 10.2 Commit Quality

Commits should be small enough to review and large enough to represent a coherent state.

Preferred progression:

```text
commit 1: tests and fixtures
commit 2: implementation
commit 3: edge-case corrections
commit 4: traceability evidence
```

### 10.3 Pull Request Template

```markdown
## Scope
<Backlog ID and title>

## Requirements
<Exact requirement IDs>

## Implementation Summary
<What changed and why>

## Files Changed
<List of source, tests, docs, migrations>

## Tests
<Exact commands>

## Latest Results
<Pass/fail counts and environment>

## PIT Review
<Findings or explicit no-blocker statement>

## Known Limitations
<Remaining limitations>

## Non-Goals
<Adjacent work intentionally excluded>

## Coverage Matrix
<Rows and evidence updated>

## Human Decisions Required
<None or precise blocked decisions>
```

### 10.4 Merge Requirements

A PR may be merged only when:

```text
targeted tests pass
Release 0 regression tests pass
requirement references validate
no BLOCKER review findings remain
no secrets are introduced
coverage evidence is accurate
human approval is present for controlled areas
```

---

## 11. Test-First and Evidence-First Rules

The implementation status progression is:

```text
DOCUMENTED
  -> DESIGNED
  -> PARTIALLY_IMPLEMENTED
  -> IMPLEMENTED_UNTESTED
  -> TESTED_RESEARCH
```

A direct transition from `PARTIALLY_IMPLEMENTED` to `TESTED_RESEARCH` is forbidden unless a real executable test ID, reproducible command, and latest passing result are recorded.

A test must verify observable behavior, not only implementation details.

Expected-output changes require review. Golden fixtures must not be rewritten merely to make a failing implementation pass.

A downstream component must not compensate for an upstream contract failure.

---

## 12. CLAUDE.md Contract

The repository-root `CLAUDE.md` should remain concise and must include:

```markdown
# Authority
The canonical specification is authoritative.
The coverage matrix is the implementation-evidence source of truth.

# Current Scope
Work only on Release 0 unless a task explicitly states otherwise.

# Dependency Order
1. Requirement reference validation
2. Canonical OHLCV
3. PIT labels
4. Training/latest schema parity
5. Checkpoint and resume
6. Purged walk-forward
7. Baseline evidence

# Forbidden Release 0 Work
Do not implement FinBERT, sequence models, graph models,
broker execution, paper trading, live trading, or new product requirements.

# Git Rules
Never push directly to main.
Use one branch per slice.
Never force-push shared branches.
Never auto-merge controlled financial logic.

# Evidence Rules
Never mark TESTED_RESEARCH without a test ID,
reproducible command, latest passing result, code location,
and independent review.

# Security
Never read or modify secrets, credentials, .env files,
broker keys, or restricted data.
```

Long procedures should be implemented as Claude Code skills rather than expanding `CLAUDE.md` indefinitely.

---

## 13. Recommended Claude Skills

Recommended reusable workflows:

```text
/validate-spec
/inventory-release0-code
/plan-release0-slice
/implement-release0-slice
/review-pit
/review-diff
/run-release0-gates
/update-coverage-matrix
/generate-autonomous-report
```

A slice implementation skill should execute:

```text
1. Read exact requirements.
2. Verify dependencies.
3. Inspect existing code.
4. Define the target contract.
5. Add or validate tests.
6. Implement the smallest coherent change.
7. Run targeted tests.
8. Run Release 0 regression tests.
9. Request independent review.
10. Update coverage only after evidence exists.
```

---

## 14. Hook and CI Enforcement

Natural-language instructions guide behavior. Hooks and CI enforce behavior.

### 14.1 Pre-Tool or Pre-Commit Controls

Block or flag:

```text
reading .env or credential paths
committing secrets
push to main
force-push
removing tests
modifying golden fixtures without approval
modifying canonical thresholds during implementation
unsafe destructive shell commands
```

### 14.2 Post-Edit Controls

After Python edits:

```text
formatter
linter
type checker
targeted unit tests
```

### 14.3 Stop-Gate Controls

Before an agent can claim completion:

```text
pytest tests/release0
requirement-reference validator
coverage-matrix validator
secret scan
git diff --check
unresolved review finding check
```

### 14.4 CI Required Checks

Recommended protected-branch checks:

```text
release0-tests
lint
static-type-check
requirement-reference-validation
coverage-matrix-validation
secret-scan
PIT-review-status
```

---

## 15. Autonomous Multi-Day Operation

### 15.1 Allowed Autonomous Actions

```text
read repository and controlled documents
create issues
create branches
create commits
push feature branches
run tests
open pull requests
review pull requests
address review findings
update implementation documentation
mark tasks READY or BLOCKED
```

### 15.2 Forbidden Autonomous Actions

```text
push directly to main
merge controlled PRs
change risk or readiness thresholds
enable broker connectivity
access broker credentials
execute trades
promote to PAPER or LIVE
claim Release 0 complete without passing blockers
silently invent missing financial rules
```

### 15.3 Autonomous Controller Loop

```text
1. Read backlog and matrix.
2. Select the first dependency-safe open slice.
3. Validate requirement references.
4. Create or refine the GitHub issue.
5. Start the test and implementation workflow.
6. Open the PR.
7. Trigger independent review and CI.
8. Address BLOCKER and MAJOR findings.
9. Mark READY or BLOCKED.
10. Continue to the next eligible slice.
```

### 15.4 Completion Condition

The autonomous run completes when either:

```text
A. every Release 0 slice has a reviewed PR with passing deterministic gates; or

B. every remaining slice is BLOCKED with the exact missing decision,
affected requirement IDs, evidence gathered, and the smallest human action needed.
```

### 15.5 Required Autonomous Report

The controller must create:

```text
docs/AUTONOMOUS_RELEASE_0_REPORT.md
```

The report must include:

```text
completed slices
open pull requests
passing test commands
latest test results
coverage matrix changes
unresolved findings
blocked decisions
files changed
commit references
artifact hashes when relevant
recommended human review order
next safe action
```

---

## 16. `/goal` Usage Policy

A goal must be bounded and objectively verifiable.

Good example:

```text
R0-BL-003 is complete only when:
- one canonical OHLCV adapter exists;
- raw provider column layouts do not reach downstream feature code;
- tests/release0/test_ohlcv_adapter.py passes;
- flat and MultiIndex fixtures are covered;
- duplicate timestamps and non-numeric fields fail explicitly;
- the full Release 0 suite passes;
- an independent reviewer reports no BLOCKER findings;
- coverage rows contain real test evidence.
```

Bad example:

```text
Build the entire AI trading platform.
```

A model-evaluated goal must be combined with deterministic CI and stop hooks. A model's statement that a goal is complete is not sufficient evidence.

---

## 17. Security and Data Boundaries

Agents must not access:

```text
broker credentials
withdrawal-enabled keys
.env files
personal secrets
production databases
restricted article bodies without license approval
live trading accounts
```

Secrets must be supplied through an approved secret manager or CI secret facility and exposed only to the minimum required workflow.

Agent prompts, logs, pull requests, and reports must redact:

```text
credentials
broker account identifiers
restricted provider data
licensed article bodies
personal data
```

No agent-generated code may connect to a live broker during Release 0 or Release 1A.

---

## 18. Human Control Points

Human review is mandatory for:

```text
canonical requirement changes
schema changes affecting sources of truth
label definitions
PIT availability policies
golden-fixture expectation changes
validation and holdout rules
risk and portfolio rules
readiness thresholds
broker and execution work
merge to main for controlled financial logic
```

Human review should focus first on:

```text
semantic correctness
temporal assumptions
financial definitions
failure behavior
unintended scope changes
```

Style and formatting issues should be automated where possible.

---

## 19. Failure and Blocked-State Policy

An agent must stop or mark the task blocked when:

```text
a canonical requirement is contradictory
an essential threshold is missing
a schema owner is ambiguous
a required data source is unavailable
licensing prevents the proposed persistence model
a deterministic test cannot be designed from the current contract
upstream gate evidence is missing
```

A blocked record must contain:

```text
blocking issue
requirement IDs
files or modules affected
evidence already collected
attempted alternatives
why guessing is unsafe
smallest human decision needed
independent tasks that can continue
```

Blocked is a valid and preferable outcome to fabricated completion.

---

## 20. Definition of Done for an Implementation Slice

A slice is complete only when:

```text
scope is bounded
requirement references are valid
code location is canonical
failure behavior is explicit
targeted tests pass
Release 0 regression tests pass
PIT review has no unresolved BLOCKER
CI checks pass
PR is reviewable
coverage matrix contains real evidence
no unrelated scope was added
```

A merged slice must remain reproducible from a clean checkout using documented commands.

---

## 21. Initial Implementation Plan

The recommended initial GitHub issue sequence is:

```text
R0-000 Validate and repair REQ-* references
R0-001 Create repository controls, CLAUDE.md, agents, hooks, and CI
R0-002 Inventory existing Release 0 code and duplicates
R0-003 Build canonical OHLCV tests and adapter
R0-004 Build PIT labels for 5, 8, and 14 sessions
R0-005 Build training/latest schema parity and feature schema hashing
R0-006 Build deterministic checkpoint and resume tests
R0-007 Build purged walk-forward and embargo
R0-008 Build approved baseline and reproducible report
R0-009 Reconcile coverage matrix and produce Release 0 evidence report
```

The controller must not reorder dependent issues merely because later work appears more interesting or easier.

---

## 22. Master Autonomous Controller Instruction

The following instruction may be used after repository permissions, CI, hooks, and branch protection are configured:

```text
You are the autonomous Release 0 delivery controller for this repository.

Treat the canonical specification as the highest authority and the coverage
matrix as the source of truth for implementation evidence.

Close as much of Release 0 as possible in this order:

1. Requirement-reference validation.
2. Canonical OHLCV adapter.
3. PIT labels for 5, 8, and 14 exchange sessions.
4. training_df/latest_features_df schema parity.
5. Deterministic checkpoint and resume.
6. Purged walk-forward validation and embargo.
7. Approved baseline model and reproducible report.

For each slice:
- verify dependencies;
- cite exact requirement IDs;
- inspect existing code before creating new code;
- create a dedicated branch;
- add tests before or with implementation;
- run targeted and full Release 0 tests;
- request independent PIT and code review;
- address all BLOCKER and MAJOR findings;
- open a pull request;
- update coverage only with real evidence.

Do not implement deferred capabilities. Do not push to main. Do not merge.
Do not change financial, risk, calibration, or readiness thresholds.
Do not access secrets or broker systems.

When blocked, record the exact missing decision and continue with another
independent task if possible.

The run is complete only when every Release 0 slice is READY with passing
reviewed evidence or BLOCKED with a precise human decision request.

Produce docs/AUTONOMOUS_RELEASE_0_REPORT.md before stopping.
```

---

## 23. Final Operating Principle

The project should not be built by asking one model to generate the full system in one pass.

It should be built through a controlled sequence:

```text
small requirement slice
  -> isolated branch
  -> executable tests
  -> minimal implementation
  -> independent temporal review
  -> CI evidence
  -> pull request
  -> human merge
```

The quality of the agentic system is measured not by how much code it writes, but by how reliably it turns canonical requirements into reviewable, reproducible, point-in-time-safe implementation evidence.
