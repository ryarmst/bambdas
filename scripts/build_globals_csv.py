#!/usr/bin/env python3
"""
Generate globals.csv from burpglobal: metadata in all .bambda files.

Reads every *.bambda file in the repo, extracts the burpglobal: YAML block,
and writes a globals.csv in the Burp Globals import/export format:
  name,value,regex   (no header row; regex column left empty)

Duplicate names are deduplicated — the first occurrence wins (alphabetical
file order). Conflicting default values emit a warning to stderr.
"""

import csv
import glob
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML is required: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


def _yaml_value_to_str(value) -> str:
    """Convert a YAML-parsed Python value back to a Burp Globals string."""
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return ""
    return str(value)


def extract_globals(bambda_path: Path) -> dict:
    """
    Parse a .bambda file and return its burpglobal: block as an ordered dict
    mapping variable name -> default value string.
    """
    try:
        with open(bambda_path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        print(f"WARNING: could not parse {bambda_path}: {exc}", file=sys.stderr)
        return {}

    if not isinstance(data, dict):
        return {}

    block = data.get("burpglobal")
    if not block or not isinstance(block, dict):
        return {}

    return {name: _yaml_value_to_str(val) for name, val in block.items()}


def main() -> None:
    repo_root = Path(__file__).parent.parent
    bambda_files = sorted(repo_root.glob("**/*.bambda"))

    if not bambda_files:
        print("No .bambda files found.", file=sys.stderr)
        sys.exit(1)

    # Collect entries in stable order; first occurrence wins on duplicate names.
    entries: dict[str, tuple[str, Path]] = {}  # name -> (value, source_file)

    for bambda_path in bambda_files:
        for name, value in extract_globals(bambda_path).items():
            if name in entries:
                existing_val, existing_file = entries[name]
                if existing_val != value:
                    print(
                        f"WARNING: '{name}' has conflicting defaults: "
                        f"{existing_file.name}={existing_val!r} vs "
                        f"{bambda_path.name}={value!r} — keeping {existing_file.name} value",
                        file=sys.stderr,
                    )
            else:
                entries[name] = (value, bambda_path)

    output = repo_root / "globals.csv"
    with open(output, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, lineterminator="\n")
        for name, (value, _) in entries.items():
            writer.writerow([name, value, ""])

    print(f"Wrote {len(entries)} entries to {output.relative_to(repo_root)}")
    for name, (value, src) in entries.items():
        print(f"  {name},{value},  ({src.name})")


if __name__ == "__main__":
    main()
