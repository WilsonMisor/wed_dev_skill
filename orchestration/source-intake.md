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

For ZIP input, reject path traversal, absolute paths, drive-letter paths, symlink entries, and any extraction target that escapes the staging root. Derived extraction must never mutate the original archive.

The deterministic helper `scripts/source_intake.py` may inventory files, compute SHA-256 hashes, detect exact duplicates, classify greenfield/brownfield evidence, and safely stage a ZIP. Semantic authority and requirement extraction remain governed analysis rather than filename heuristics.

## Source authority

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
- authority status;
- duplicate group;
- supersedes/superseded-by relationship;
- source-conflict group;
- missing or stale source status;
- observed, declared and approved technology-stack facts separately;
- observed, declared and approved architecture facts separately;
- extracted source requirements with stable derived IDs and original wording/location;
- assumptions, unknowns, role gaps, and decisions requiring human authority.

Project-specific derived intake state belongs under `.ai-product-delivery/source-intake/` in the application repository. Suggested artifacts are `SOURCE-INTAKE.json`, a generated `SOURCE-INTAKE.md`, `source-manifest.json`, and `source-conflicts.json`. Reuse an existing canonical project artifact when it already owns the same information instead of creating duplicate truth.

## Stable source requirement IDs

When requirements already exist in supplied sources, derive stable IDs such as `SRCREQ-0001` while preserving:

- source ID;
- source location/page/heading/line where available;
- original wording;
- normalized interpretation;
- authority level;
- confidence;
- conflict state.

The derived ID does not rewrite the original source.

## Source conflicts

If authoritative sources disagree and authority cannot resolve the disagreement, record `SOURCE CONFLICT`, identify the affected topics/requirements, and stop affected downstream work. Never silently choose a winner.

## Source drift

Bind authoritative intake sources by hash. When a bound source changes, perform impact analysis across affected PRD/SRS/SRD requirements, architecture, ADRs, risks, controls, AI Task Packets, tests, evidence, monitoring, recovery/reconciliation, and production gates. Materially affected evidence becomes stale until revalidated.

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

Stop the affected work for unresolved source conflict, unsafe archive content, missing required source, unbounded authority ambiguity, or a material source change that has not completed impact analysis.
