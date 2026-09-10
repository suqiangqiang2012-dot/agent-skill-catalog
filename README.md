# Agent Skill Catalog

Public metadata registry for independently versioned Agent Skill repositories.

The catalog may list private skills, but it never contains private source, scripts,
references, templates, or release assets.

## Validation

```text
python scripts/validate_catalog.py catalog.json
```

An entry becomes `active` only after its repository coordinate is configured and
its first stable GitHub Release is published.

Latest versions are not duplicated in the catalog. Update clients query each
repository's latest stable Release.

