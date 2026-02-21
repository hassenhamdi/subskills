#!/usr/bin/env bash
# SubSkills SessionStart Hook
# Ensures the agent is aware of its orchestration capabilities at start.

set -euo pipefail

# Determine plugin root directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
PLUGIN_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# Read the SubSkills skill content
subskills_skill_content=$(cat "${PLUGIN_ROOT}/skills/subskills/SKILL.md" 2>&1 || echo "Error reading SubSkills skill")

# Escape string for JSON embedding
escape_for_json() {
    local s="$1"
    s="${s//\/\}"
    s="${s//"/"}"
    s="${s//$'
'/
}"
    s="${s//$''/}"
    s="${s//$'	'/	}"
    printf '%s' "$s"
}

subskills_escaped=$(escape_for_json "$subskills_skill_content")
session_context="<EXTREMELY_IMPORTANT>
You have **SubSkills** active.

**Skill orchestration capabilities are now operational. Below is the pipeline configuration:**

${subskills_escaped}

**Use the 'subskills_pipeline.py' script for all high-complexity engineering tasks.**
</EXTREMELY_IMPORTANT>"

# Output JSON for Gemini CLI
cat <<EOF
{
  "allow": true,
  "context": "${session_context}"
}
EOF

exit 0
