#!/usr/bin/env bash
# SubSkills (SubSkills) Auto-Installation Script

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}--- SKILL ORCHESTRATOR: INITIATING INSTALLATION ---${NC}"

# 1. Check Prerequisites
echo -e "
[1/4] Checking prerequisites..."
if ! command -v gemini &> /dev/null; then
    echo -e "${RED}Error: Gemini CLI is not installed. Please install it first: https://geminicli.com${NC}"
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed. It is required for SubSkills orchestrators.${NC}"
    exit 1
fi
echo -e "${GREEN}Prerequisites met.${NC}"

# 2. Link Extension
echo -e "
[2/4] Linking SubSkills extension to Gemini CLI..."
gemini extensions link .
echo -e "${GREEN}Extension linked successfully.${NC}"

# 3. Enable Experimental Features
echo -e "
[3/4] Enabling Subagents and Hooks in settings.json..."
SETTINGS_FILE="$HOME/.gemini/settings.json"

# Create settings.json if it doesn't exist
if [ ! -f "$SETTINGS_FILE" ]; then
    mkdir -p "$(dirname "$SETTINGS_FILE")"
    echo "{}" > "$SETTINGS_FILE"
fi

# Use Python to robustly update JSON without destroying other settings
python3 <<EOF
import json
import os

path = "$SETTINGS_FILE"
try:
    with open(path, 'r') as f:
        data = json.load(f)
except Exception:
    data = {}

if 'experimental' not in data:
    data['experimental'] = {}

data['experimental']['enableAgents'] = True
data['experimental']['enableHooks'] = True

with open(path, 'w') as f:
    json.dump(data, f, indent=2)
EOF

echo -e "${GREEN}Subagents and Hooks enabled in $SETTINGS_FILE.${NC}"

# 4. Set Permissions
echo -e "
[4/4] Finalizing system permissions..."
chmod +x scripts/*.py
chmod +x hooks/*.sh
echo -e "${GREEN}Permissions set.${NC}"

echo -e "
${BLUE}--- INSTALLATION COMPLETE ---${NC}"
echo -e "The Skill Cache is active. You can now use the orchestration pipeline."
echo -e "Try: ${GREEN}python3 scripts/subskills_pipeline.py "Your task"${NC}"
