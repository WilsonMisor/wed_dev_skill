# Project Runtime Layout

The application repository remains the execution surface. Framework repositories are not copied wholesale into each application.

```text
application-repo/
  AGENTS.md                         # thin project operating instructions
  .codex/
    config.toml                     # project-specific Codex config where needed
    agents/                         # only project-scoped custom agents or overrides
  .agents/
    skills/                         # optional pinned repo-scoped skill links/copies
  .ai-product-delivery/
    classification/
    sources/
    requirements/
    architecture/
    task-packets/
    traceability/
    approvals/
    handoffs/
  .preos/ or configured PREOS state reference/
    project-contract/
    checkpoints/
    evidence/
    gate-results/
    risk-selections/
  src/ ...                          # application code
```

Exact runtime paths must be supplied by the owning Blueprint and PREOS repositories. This layout is an integration model, not permission for Codex to invent missing directories when the installed framework specifies different canonical paths.
