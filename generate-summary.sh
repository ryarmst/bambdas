#!/usr/bin/env bash
# Reads YAML frontmatter from each *.md file that has a matching *.bambda file
# and writes summary.md containing a markdown table of name, type, and summary.

set -euo pipefail

OUT="summary.md"
TMPFILE=$(mktemp)

extract() {
    local file="$1" field="$2"
    # Match "field: value" within the opening --- ... --- block.
    awk -v field="$field" '
        /^---$/ { count++; next }
        count == 1 && $0 ~ "^" field ": " {
            sub("^" field ": ", ""); print; exit
        }
        count >= 2 { exit }
    ' "$file"
}

{
    echo "| Name | Type | Gate | Summary |"
    echo "|---|---|---|---|"
    for bambda in *.bambda; do
        base="${bambda%.bambda}"
        md="${base}.md"
        [[ -f "$md" ]] || continue
        name=$(extract "$md" "name")
        type=$(extract "$md" "type")
        gate=$(extract "$md" "gate")
        summary=$(extract "$md" "summary")
        echo "| $name | \`$type\` | \`$gate\` | $summary |"
    done
} > "$TMPFILE"

{
    echo "# Bambda Summary"
    echo ""
    echo "Generated from bambda \`.md\` files. Run \`./generate-summary.sh\` to regenerate."
    echo ""
    cat "$TMPFILE"
} > "$OUT"

rm "$TMPFILE"
echo "Written: $OUT"
