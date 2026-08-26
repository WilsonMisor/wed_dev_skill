# Governed Project Source Intake

Use this stage before discovery when the user supplies a documentation package, ZIP archive, existing repository, brownfield codebase, mixed historical/current files, or any source set whose authority is not already clear.

Source intake is a Blueprint lifecycle capability. It establishes what material exists and which material may govern downstream work. It does **not** create the PREOS Project Contract and it does not replace PRD, SRS, SRD, ADRs, or approved architecture.

## Inputs

Accepted inputs may include:

1. a directory of documents;
2. a ZIP archive;
3. an existing repository;
4. a repository plus supporting documentation;
5. a greenfield project pack;
6. a brownfield or migration project;
7. individual files plus a short intent statement.

## Safety boundary

Intake is inspection, not execution. Do not run installers, macros, package lifecycle hooks, migrations, application startup, arbitrary shell/PowerShell/Python/PHP/Node scripts, unknown binaries, or project builds merely to understand the package.

For ZIP input, reject path traversal, absolute paths, drive-letter paths, symlink entries, reparse/junction entries, and any extraction target that escapes the staging root. Derived extraction must never mutate the original archive or overwrite staged content with different bytes.

The deterministic helper `scripts/source_intake.py` inventories files, computes SHA-256 hashes, detects exact duplicates and conservative filename-version/revision **candidates**, classifies greenfield/brownfield evidence, and safely stages a ZIP. Version candidates are the conservative near-duplicate/revision signal; they never establish byte equivalence, authority, or supersession. It never promotes a filename such as `final.docx` into authority and never infers supersession merely because one file looks newer.

## Governed decision input

Semantic judgments are explicit inputs, not filename heuristics. The helper may receive a governed JSON decisions document with:

- `project_mode`;
- `source_decisions` for authority, status, explicit supersession, conflict group, topic and declared version;
- `source_requirements` preserving original wording and source location;
- observed, declared and approved architecture separately;
- observed, declared and approved technology stack separately;
- assumptions, unknowns, role gaps and human decisions required.

The helper validates those relationships and derives reproducible intake artifacts. It must reject unknown source references, invalid authority/status values and malformed governed input rather than guessing.

## Source authority

Every newly inventoried source starts as **`UNCLASSIFIED`** until governed analysis assigns an authority level. `UNCLASSIFIED` is not equivalent to approved, current, authoritative, or safe to use for implementation.

The deterministic authority enums corresponding to this precedence are `HUMAN_APPROVED`, `DECLARED_PRIMARY`, `APPROVED_SUPPORTING`, `IMPLEMENTATION_EVIDENCE`, `DRAFT_REFERENCE_HISTORY`, `UNCLASSIFIED`, and `UNRESOLVED_CONFLICT`.

Use this precedence model unless an explicit project rule overrides it:

1. **Explicit human-approved decision** — highest authority until superseded or revoked.
2. **Declared primary source of truth** — authoritative for its declared topic.
3. **Approved supporting specification** — subordinate detail consistent with the primary source.
4. **Current implementation evidence** — code/schema/tests show what exists, but do not silently override approved requirements.
5. **Draft/reference/history** — context only; do not silently promote it.
6. **Unresolved source conflict** — block affected downstream work.

A filename such as `final.docx`, a newer timestamp, or an implementation that happens to exist is not sufficient to establish authority.

## Required intake record

Record, as applicable:

- project mode: `GREENFIELD`, `BROWNFIELD`, `HYBRID_OR_MIGRATION`, or `UNKNOWN`;
- source ID, relative/original path, type, size, SHA-256 and ingestion time;
- authority status, initially `UNCLASSIFIED` until deliberately resolved;
- exact duplicate group;
- version-candidate group, explicitly non-authoritative;
- supersedes/superseded-by relationship only when explicitly governed;
- source-conflict group and whether it remains blocking;
- missing or stale source status;
- observed, declared and approved technology-stack facts separately;
- observed, declared and approved architecture facts separately;
- extracted source requirements with stable derived IDs and original wording/location;
- assumptions, unknowns, role gaps, and decisions requiring human authority.

Project-specific derived intake state belongs under `.ai-product-delivery/source-intake/` in the application repository. Suggested artifacts are `SOURCE-INTAKE.json`, a generated `SOURCE-INTAKE.md`, `source-manifest.json`, and `source-conflicts.json`. Reuse an existing canonical project artifact when it already owns the same information instead of creating duplicate truth.

## Duplicate, version and supersession rules

Exact byte duplicates may be grouped deterministically by SHA-256. Filename families such as `requirements-v1.md` and `requirements-final.md` may be reported as **version candidates only**. A candidate group does not establish which file is current.

Supersession is recorded only from an explicit governed decision. When source B explicitly supersedes source A, record the reciprocal `supersedes` / `superseded_by` relationship and mark A superseded unless an explicit status says otherwise.

## Stable source requirement IDs

When requirements already exist in supplied sources, derive stable IDs such as `SRCREQ-0001` while preserving:

- source ID;
- source location/page/heading/line where available;
- original wording;
- normalized interpretation;
- authority level;
- confidence;
- conflict state.

For a fixed governed requirement set, derive IDs from a stable semantic sort rather than incoming JSON order, so reordering the decision file does not silently renumber requirements. The derived ID does not rewrite the original source.

## Source conflicts

If different content is explicitly placed in the same conflict group, the conflict may be resolved only when one source has a unique higher governed authority. Equal-authority or unclassified competing content remains `SOURCE CONFLICT` and blocks affected downstream work. Exact byte duplicates are not a content conflict.

If authoritative sources disagree and authority cannot resolve the disagreement, record `SOURCE CONFLICT`, identify the affected topics/requirements, and stop affected downstream work. Never silently choose a winner.

## Source drift

Bind authoritative intake sources by hash. When a bound source changes, perform impact analysis across affected PRD/SRS/SRD requirements, architecture, ADRs, risks, controls, AI Task Packets, tests, evidence, monitoring, recovery/reconciliation, and production gates. Materially affected evidence becomes stale until revalidated.

For deterministic re-intake, supply an immutable prior `source-manifest.json` through `--baseline-manifest`. The helper compares previously `HUMAN_APPROVED`, `DECLARED_PRIMARY`, and `APPROVED_SUPPORTING` source hashes, reports changed or missing authoritative sources, and blocks affected downstream work until the required impact analysis is completed. The baseline manifest must be separate from the output manifest so drift evidence cannot overwrite its own comparison baseline.

## Handoff

The corrected lifecycle is:

```text
Source Intake
    -> Blueprint Discovery
    -> PRD
    -> Project Classification
    -> PREOS project-init when active
    -> PREOS Project Contract
```

PREOS project-init compiles the hash/version-bound production-assurance Project Contract from approved Blueprint truth. Source intake must not create a competing contract.

## Stop conditions

Stop the affected work for unresolved source conflict, unsafe archive content, missing required source, unbounded authority ambiguity, invalid governed decision input, or a material source change that has not completed impact analysis.
