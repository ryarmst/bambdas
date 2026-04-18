# bambdas — Claude Instructions

## Documentation standard

Every `.bambda` file must have a matching `.md` file with the same base name. Keep docs **short** — the goal is fast reference, not a tutorial.

### Required frontmatter

Each `.md` file must begin with YAML frontmatter containing exactly these fields:

```yaml
---
name: <human-readable name matching the bambda `name:` field>
type: <bambda function value, e.g. SCAN_CHECK_ACTIVE_PER_INSERTION_POINT>
gate: <burp global that enables this bambda, e.g. bambda-fuzzing>
summary: <one or two sentences — what it does, what it finds, and any key behaviour worth knowing at a glance>
---
```

The `summary` field is machine-read by `generate-summary.sh` to build `summary.md`. Write it to stand alone in a table cell: no markdown, no code fences, under 200 characters.

### Body sections (use only what applies)

```markdown
## Globals

| Global | Default | Purpose |
|---|---|---|
| `global-name` | `value` | one-line description |

## Notes

- Bullet points only.
- Cover non-obvious behaviour, gotchas, and tuning hints.
- No background theory. No step-by-step calibration guides.
- Anything self-evident from the globals table does not need a note.
```

Do not add any other sections. Do not add import instructions — those belong in the README.

### What to omit

- How Burp's internal algorithms work
- Generic vulnerability background (WAF behaviour, injection classes)
- Step-by-step calibration walkthroughs
- Anything already in the README

---

## summary.md workflow

Run `./generate-summary.sh` to regenerate `summary.md` from all bambda `.md` files. The script reads the YAML frontmatter from each `.md`, extracts `name`, `type`, and `summary`, and writes a markdown table.

When adding a new bambda:
1. Write the `.bambda` file.
2. Write a matching `.md` file following the format above.
3. Run `./generate-summary.sh` to update `summary.md`.
4. Update `globals.csv` if the bambda introduces new Burp Globals.
