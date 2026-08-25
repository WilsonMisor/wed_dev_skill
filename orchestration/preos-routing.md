# PREOS Production Assurance Routing

PREOS is the Production Risk, Economics, and Evolution Operating System. Within the integrated delivery system it is an assurance overlay governed by the AI Product Delivery Blueprint. It is not a replacement for product requirements, architecture ownership, gstack specialist judgment, Codex implementation, or accountable human authority.

## Responsibility model

1. The AI Product Delivery Blueprint governs lifecycle, approved baselines, active profiles, required artifacts, approval gates, and change control.
2. PREOS evaluates production risk, economics, evidence validity, operational readiness, deferred complexity, release risk, and production learning against those approved baselines.
3. gstack supplies specialist review and challenge when PREOS or the Blueprint routes work to an engineering role.
4. Codex implements approved AI Task Packets in the application repository.
5. Accountable humans accept consequential risk and authorize production deployment.
6. The application repository stores project-specific governance state under `.ai-product-delivery/`, while PREOS runtime/recovery state uses `PREOS_STATE_ROOT`.

Do not merge or vendor the Blueprint, PREOS, gstack, and application repositories merely to make them cooperate. Integrate through installed skills, versioned contracts, project artifacts, risk/control/evidence IDs, and explicit handoffs.

## Assurance classification

Record one PREOS assurance level in the Project Classification Record:

1. `inactive`: disposable experiment with no production users, sensitive data, consequential action, durable business dependency, or meaningful external exposure.
2. `lightweight`: early prototype or internal pilot with limited consequence; apply Project Contract, relevant baseline controls, contextual risk selection, and a reduced release check.
3. `standard`: normal production software; apply the full PREOS lifecycle proportionate to active profiles and risks.
4. `high-assurance`: software with significant money movement, multi-tenancy, sensitive data, safety/security exposure, regulatory obligations, high operational consequence, or large blast radius; require explicit G0-G11 evidence and accountable risk acceptance.

The assurance level controls depth, not whether hard production risks may be ignored. A control that is structurally required by the product remains required even under a lower assurance level.

## PREOS maturity model

Record the current maturity stage and reassess it when product conditions change:

- Stage 0: Prototype.
- Stage 1: Early Production.
- Stage 2: Product Traction.
- Stage 3: Scaling Product.
- Stage 4: Large Platform.
- Stage 5: High Assurance / Global.

Architecture complexity must follow measured activation triggers rather than speculative scale assumptions.

## Lifecycle routing

### After PRD and Project Classification

Run `preos-project-init` when PREOS is active. It creates or refreshes the Project Contract as a hash-bound snapshot of approved product, system, build, architecture, classification, authority, maturity, vendor, and environment truth.

The Project Contract does not replace the Project Charter, PRD, SRS, SRD, ADRs, or Project Classification Record. It binds PREOS to their approved versions and detects source drift.

### Risk Pass A: product and classification

Run `preos-risk-model` after PRD/classification to identify business-rule, trust-boundary, tenant, financial, privacy, abuse, operational, and other early risks. Always include the deterministic 75-control baseline, then select relevant records from the canonical risk catalogue and generate contextual combinations when necessary.

### During architecture

Run `preos-architecture-economics` together with architecture work and `gstack-plan-eng-review` where applicable.

For important architecture choices, capture:

- cost now and expected cost at later maturity stages;
- variable cost drivers;
- operational and specialist burden;
- vendor concentration and migration exposure;
- failure cost;
- complexity tax;
- activation assumption;
- measurable activation trigger;
- migration path;
- review trigger.

Record justified deferred infrastructure or architecture in the Deferred Complexity Registry instead of adding speculative complexity immediately.

### Risk Pass B: architecture

After architecture is sufficiently concrete, rerun `preos-risk-model` for architecture-dependent risks such as data integrity, queues, retries, caches, search, external vendors, API compatibility, mobile-version skew, scaling, recovery, and economic abuse.

### Before each substantial implementation packet

Run a risk delta/change-impact pass for the specific change. Extend the canonical AI Task Packet rather than inventing a competing PREOS implementation unit.

The packet should include when applicable:

- PREOS risk IDs;
- baseline/control IDs;
- applicable G0-G11 gates;
- evidence requirements and freshness bindings;
- failure tests;
- monitoring;
- recovery and reconciliation;
- economic/complexity effects;
- human risk owner and approver.

Then run `preos-production-plan` to produce or enrich the bounded packet.

### During implementation

Use Codex under the approved packet. `preos-production-implement` evaluates the change against the packet and PREOS constraints but does not silently expand scope or grant itself authority.

Route specialist needs through gstack, including as applicable:

- architecture uncertainty -> `gstack-plan-eng-review`;
- security risk -> `gstack-cso`;
- implementation review -> `gstack-review`;
- root-cause uncertainty -> `gstack-investigate`;
- browser/workflow evidence -> `gstack-qa` or `gstack-qa-only`;
- performance evidence -> `gstack-benchmark`;
- release preparation -> `gstack-ship`;
- deployment -> `gstack-land-and-deploy` after human approval;
- canary verification -> `gstack-canary`;
- retrospective -> `gstack-retro`.

PREOS decides what assurance evidence is required. gstack supplies specialist review. Neither may silently change an approved Blueprint baseline.

## Release assurance: G0-G11

Before production, evaluate the PREOS production gates as applicable:

- G0 Source / Project Contract.
- G1 Product / Business Correctness.
- G2 Architecture.
- G3 Security / Identity / Trust / Privacy.
- G4 Data Correctness.
- G5 Financial Correctness / Economics.
- G6 Performance / Capacity.
- G7 Failure / Recovery.
- G8 Change / Deployment Safety.
- G9 Operations / Support.
- G10 Legal / Compliance / Accessibility.
- G11 Evidence / Authority.

These gates supplement rather than replace Blueprint lifecycle gates. A PREOS RED, unresolved HUMAN REVIEW, or material UNKNOWN on a required gate prevents a Blueprint production pass unless an accountable human uses a permitted, documented risk-acceptance path.

## Deterministic state semantics

Allowed PREOS states are:

- GREEN;
- AMBER;
- RED;
- HUMAN REVIEW;
- UNKNOWN.

`UNKNOWN` never silently becomes `GREEN`. Absence of evidence is not evidence of safety.

Control dependencies must propagate. A downstream control or gate cannot become GREEN when a required prerequisite remains RED or UNKNOWN unless the governing rule explicitly permits that state with documented rationale.

## Evidence freshness

Evidence must bind to the source state that produced it, including relevant artifact versions/hashes, commit, environment, schema/configuration/dependency state, test version, and timestamp when applicable.

A material change invalidates or marks stale the evidence it affects. Change-impact analysis must identify which controls, tests, monitors, recovery assumptions, risk decisions, and gate results require reevaluation.

## Human authority

AI roles, PREOS, Codex, and gstack may analyse and recommend. They cannot impersonate an accountable human risk owner, DPO, legal authority, financial authority, security approver, production owner, or other decision-right holder.

If a required accountable role does not exist, record a role gap and route to HUMAN REVIEW. Do not fill the gap by assigning an AI persona.

Risk acceptance must identify the accountable human authority, rationale, scope, expiry/review condition, compensating controls where required, and the specific risks/controls/gates accepted.

## Project and runtime state

Version-controlled project state belongs under:

```text
.ai-product-delivery/
  project-contract/
  task-packets/
  preos/
    risk-model/
    control-assessments/
    architecture-economics/
    deferred-complexity/
    gate-state/
    evidence/
    risk-acceptance/
    incidents/
    traceability/
  approvals/
```

Runtime/recovery state belongs under independent `PREOS_STATE_ROOT`, not `.gstack` or `GSTACK_STATE_ROOT`.

Conversation memory is never the authoritative record of production assurance state.

## Production learning loop

After deployments, incidents, near misses, support findings, security findings, cost anomalies, reliability events, or major operational lessons, run `preos-production-learn`.

Accepted learning may create or update:

- risk rules;
- regression tests;
- controls;
- monitoring;
- runbooks/recovery logic;
- evidence invalidation rules;
- ADR review triggers;
- Deferred Complexity activation triggers;
- future task packets.

Feed accepted changes through Blueprint change control. PREOS learning does not silently mutate approved requirements or architecture.

## Stop conditions

Stop or escalate the affected work when:

1. the Project Contract is stale or cannot bind to approved source artifacts;
2. required PREOS source data fails integrity validation;
3. a critical risk/control/gate is RED;
4. required evidence is missing, stale, or UNKNOWN;
5. a required accountable human authority is missing;
6. risk acceptance is invalid, expired, or outside the accepter's authority;
7. control dependencies make a downstream GREEN claim impossible;
8. production economics or complexity assumptions are materially unsupported;
9. change impact cannot be bounded safely;
10. PREOS, gstack, Codex, or project artifacts conflict with the approved Blueprint baseline and no human resolution exists.