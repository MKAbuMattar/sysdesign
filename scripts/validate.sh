#!/usr/bin/env bash
# Validate the sysdesign plugin. No build — just the invariants the docs promise.
# Single source of truth: CI (.github/workflows/validate.yml) and contributors both run this.
# Usage: bash scripts/validate.sh
set -euo pipefail

cd "$(git rev-parse --show-toplevel 2>/dev/null || dirname "$(dirname "$(readlink -f "$0")")")"

fail=0
ok()   { printf '  OK   %s\n' "$1"; }
bad()  { printf '  FAIL %s\n' "$1"; fail=1; }

# 1. Manifests parse and versions match.
if python3 - <<'PY'
import json, sys
p = json.load(open(".claude-plugin/plugin.json"))
m = json.load(open(".claude-plugin/marketplace.json"))
sys.exit(0 if p["version"] == m["plugins"][0]["version"] else 1)
PY
then ok "manifests parse, versions match"; else bad "manifests invalid or version mismatch"; fi

# 2. Skill is self-contained: no external links anywhere under skills/.
if grep -rqE 'https?://' skills; then
  bad "external link(s) in skills/ — must be self-contained:"; grep -rnE 'https?://' skills | sed 's/^/       /'
else ok "no external links in skills/"; fi

# 3. Every reference file has a row in the SKILL.md reference map.
for f in skills/system-design/references/*.md; do
  name="references/$(basename "$f")"
  grep -q "$name" skills/system-design/SKILL.md || bad "$name not in SKILL.md map"
done
[ "$fail" -eq 0 ] && ok "all reference files mapped in SKILL.md"

# 3b. Every reference surfaces its clarify-first questions (the Ask-first convention).
miss_ask=0
for f in skills/system-design/references/*.md; do
  grep -q "AskUserQuestion" "$f" || { bad "references/$(basename "$f") has no AskUserQuestion / Ask-first note"; miss_ask=1; }
done
[ "$miss_ask" -eq 0 ] && ok "every reference has its Ask-first note"

# 4. SKILL.md and every command declare YAML frontmatter.
for f in skills/system-design/SKILL.md commands/*.md; do
  [ "$(head -1 "$f")" = "---" ] || bad "$f missing frontmatter"
done

echo
[ "$fail" -eq 0 ] && echo "validate: PASS" || { echo "validate: FAIL"; exit 1; }
