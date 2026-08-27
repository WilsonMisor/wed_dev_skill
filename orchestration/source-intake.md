# Governed Project Source Intake

Use this stage before discovery when the user supplies a documentation package, ZIP archive, existing repository, brownfield codebase, mixed historical/current files, or any source set whose authority is not already clear.

Source intake is a Blueprint lifecycle capability. It establishes what material exists, extracts candidate requirements/architecture/technology-stack facts from supported material, and establishes which material may govern downstream work. It does **not** create the PREOS Project Contract and it does not replace PRD, SRS, SRD, ADRs, or approved architecture.

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

The deterministic helper `scripts/source_intake.py` inventories files, computes SHA-256 hashes, detects exact duplicates and conservative filename-version/revision **candidates**, classifies greenfield/brownfield evidence, safely stages ZIP content when requested, and invokes the non-executing semantic extractor in `scripts/source_semantic_extract.py`. Version candidates are conservative near-duplicate/revision signals; they never establish byte equivalence, authority, or supersession. A filename such as `final.docx` never becomes authoritative merely because it looks newer or more final.

## Automatic semantic extraction

Source intake must not require a human to manually retype everything already present in the supplied material. For supported text, code, project metadata, ZIP members, and text contained in Office Open XML documents such as `.docx`/`.pptx`, the helper automatically extracts **candidates/evidence** for:

- requirements already present in supplied documents, preserving source, location and original wording;
- observed architecture inferred from repository/project structure and implementation evidence;
- architecture statements explicitly declared in supplied text;
- observed technology stack inferred from source extensions, package/project manifests and implementation evidence;
- technology-stack statements explicitly declared in supplied text.

The extractor is deterministic and non-executing. It does not run source code, install dependencies, invoke macros, execute Office content, or call project build tools.

Automatic extraction is **not approval**. Every automatically extracted semantic item remains evidence/candidate material requiring governed review where consequence or ambiguity matters. The extractor records this boundary and never creates `approved_architecture` or `approved_stack` by itself.

## Observed, declared, and approved separation

Never collapse these concepts:

- **Observed architecture / stack** — what repository structure, code and project metadata show is present.
- **Declared architecture / stack** — what supplied documents explicitly say the system uses or intends to use.
- **Approved architecture / stack** — the architecture/stack deliberately accepted by the accountable governed process.

Observed and declared values may disagree. Preserve both. Approved values come only from governed decisions, never from filename heuristics or automatic extraction.

When a governed decision supplies an observed or declared interpretation, retain the automatic extraction evidence separately rather than erasing it. The intake record distinguishes `extracted` from `governed` facts when both exist.

## Governed decision input

The helper may receive a governed JSON decisions document with:

- `project_mode`;
- `source_decisions` for authority, status, explicit supersession, conflict group, topic and declared version;
- reviewed/approved `source_requirements` that can refine or replace an automatically extracted duplicate;
- governed observed, declared and approved architecture separately;
- governed observed, declared and approved technology stack separately;
- assumptions, unknowns, role gaps and human decisions required.

The helper validates those relationships and derives reproducible intake artifacts. It must reject unknown source references, invalid authority/status values and malformed governed input rather than guessing.

A governed decision may correct or approve an extracted candidate, but it must not destroy the underlying source/evidence record that explains what was originally observed or declared.

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

A filename such as `final.docx`, a newer timestamp, an automatically extracted statement, or an implementation that happens to exist is not sufficient to establish authority.

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
- automatically observed, governed-observed, declared and approved technology-stack facts separately;
- automatically observed, governed-observed, declared and approved architecture facts separately;
- extracted source requirements with stable derived IDs and original wording/location;
- extraction method/confidence and whether governed review remains required;
- assumptions, unknowns, role gaps, and decisions requiring human authority.

Project-specific derived intake state belongs under `.ai-product-delivery/source-intake/` in the application repository. Suggested artifacts are `SOURCE-INTAKE.json`, a generated `SOURCE-INTAKE.md`, `source-manifest.json`, and `source-conflicts.json`. Reuse an existing canonical project artifact when it already owns the same information instead of creating duplicate truth.

## Duplicate, version and supersession rules

Exact byte duplicates may be grouped deterministically by SHA-256. Filename families such as `requirements-v1.md` and `requirements-final.md` may be reported as **version candidates only**. A candidate group does not establish which file is current.

Supersession is recorded only from an explicit governed decision. When source B explicitly supersedes source A, record the reciprocal `supersedes` / `superseded_by` relationship and mark A superseded unless an explicit status says otherwise.

Automatic semantic extraction may extract requirements from both an old draft and a newer candidate. That is intentional: extraction preserves evidence; authority resolution decides which requirement governs.

## Stable source requirement IDs

When requirements exist in supplied sources, derive stable IDs such as `SRCREQ-0001` while preserving:

- source ID;
- source location/page/heading/line where available;
- original wording;
- normalized interpretation;
- category;
- authority level;
- confidence;
- conflict state;
- extraction method;
- governed-review requirement.

For a fixed governed/extracted requirement set, derive IDs from a stable semantic sort rather than incoming JSON order, so reordering a decision file does not silently renumber requirements. The derived ID does not rewrite the original source.

## Source conflicts

If different content is explicitly placed in the same conflict group, the conflict may be resolved only when one source has a unique higher governed authority. Equal-authority or unclassified competing content remains `SOURCE CONFLICT` and blocks affected downstream work. Exact byte duplicates are not a content conflict.

If authoritative sources disagree and authority cannot resolve the disagreement, record `SOURCE CONFLICT`, identify the affected topics/requirements, and stop affected downstream work. Never silently choose a winner.

Extracted requirements or architecture/stack statements that disagree are preserved as candidates until governed authority/conflict resolution determines what controls downstream work.

## Source drift

Bind authoritative intake sources by hash. When a bound source changes, perform impact analysis across affected PRD/SRS/SRD requirements, architecture, ADRs, risks, controls, AI Task Packets, tests, evidence, monitoring, recovery/reconciliation, and production gates. Materially affected evidence becomes stale until revalidated.

For deterministic re-intake, supply an immutable prior `source-manifest.json` through `--baseline-manifest`. The helper compares previously `HUMAN_APPROVED`, `DECLARED_PRIMARY`, and `APPROVED_SUPPORTING` source hashes, reports changed or missing authoritative sources, and blocks affected downstream work until the required impact analysis is completed. The baseline manifest must be separate from the output manifest so drift evidence cannot overwrite its own comparison baseline.

## Handoff

The corrected lifecycle is:

```text
Source Intake
    -> automatic safe semantic candidate extraction
    -> governed source/semantic review and conflict resolution
    -> Blueprint Discovery
    -> PRD
    -> Project Classification
    -> PREOS project-init when active
    -> PREOS Project Contract
```

PREOS project-init compiles the hash/version-bound production-assurance Project Contract from approved Blueprint truth. Source intake must not create a competing contract.

## Stop conditions

Stop the affected work for unresolved source conflict, unsafe archive content, missing required source, unbounded authority ambiguity, invalid governed decision input, or a material source change that has not completed impact analysis.

Do **not** stop merely because automatic extraction found candidate information that still needs governed review; preserve it, surface the ambiguity, and route the consequential decision to the appropriate authority.
