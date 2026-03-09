#!/bin/bash
# Hook PostToolUse — logga invocazioni skill native
# Input: JSON via stdin con tool_name e tool_input
# Output: append a .claude/skill-usage.log

INPUT=$(cat)

# Estrai nome skill dal tool_input (campo "skill")
SKILL_NAME=$(echo "$INPUT" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    tool_input = data.get('tool_input', {})
    if isinstance(tool_input, str):
        tool_input = json.loads(tool_input)
    print(tool_input.get('skill', 'unknown'))
except:
    print('unknown')
" 2>/dev/null)

if [ "$SKILL_NAME" = "unknown" ] || [ -z "$SKILL_NAME" ]; then
    exit 0
fi

TIMESTAMP=$(date +"%Y-%m-%d %H:%M")
LOG_FILE="$(cd "$(dirname "$0")/../.." && pwd)/.claude/skill-usage.log"

echo "$TIMESTAMP | $SKILL_NAME | native | invoked" >> "$LOG_FILE"

exit 0
