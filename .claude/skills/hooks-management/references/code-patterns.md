# Common Hook Code Patterns

Reusable Python patterns for writing Claude Code hooks.

## Basic Hook Structure

```python
#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import read_stdin_json

def main() -> None:
    input_data = read_stdin_json()
    if not input_data:
        sys.exit(0)

    # Hook logic here
    sys.exit(0)

if __name__ == "__main__":
    main()
```

## PreToolUse Patterns

**Filter by tool name:**
```python
tool_name = input_data.get("tool_name", "")
if tool_name != "Bash":
    sys.exit(0)
```

**Extract tool input:**
```python
tool_input = input_data.get("tool_input", {})
file_path = tool_input.get("file_path", "")
command = tool_input.get("command", "")
```

**Block with reason (exit code 2):**
```python
from utils import block_response

if is_dangerous(command):
    block_response("Command blocked: contains dangerous pattern")
```

**Block with stderr:**
```python
print("Reason for blocking", file=sys.stderr)
sys.exit(2)
```

## Skill Tool Interception

**Dispatcher pattern:**
```python
SKILL_HANDLERS = {
    "skill:one": handler_one,
    "skill:two": handler_two,
}

def main() -> None:
    input_data = read_stdin_json()
    if input_data.get("tool_name") != "Skill":
        sys.exit(0)

    skill_name = input_data.get("tool_input", {}).get("skill", "")
    handler = SKILL_HANDLERS.get(skill_name)
    if handler:
        handler(input_data)
    sys.exit(0)
```

## Task Tool Interception

**Detect subagent type:**
```python
if input_data.get("tool_name") != "Task":
    sys.exit(0)

tool_input = input_data.get("tool_input", {})
subagent_type = tool_input.get("subagent_type", "")
prompt = tool_input.get("prompt", "")
```

## Guardrail Pattern

**Using GuardrailConfig and GuardrailRunner:**
```python
from utils import (
    GuardrailConfig,
    GuardrailRunner,
    create_session_file_validator,
)

config = GuardrailConfig(
    target_subagent="agent-name",
    cache_key="agent_guardrail_active",
    guarded_tools={"Write", "Edit"},
    path_validator=create_session_file_validator("subfolder", "prefix"),
)

if __name__ == "__main__":
    GuardrailRunner(config).run()
```

**Minimal guardrail:**
```python
config = GuardrailConfig(
    target_subagent="my-agent",
    cache_key="my_agent_active",
    blocked_tools={"Bash", "Write"},
)
```

## Context Injection

**Add context to session:**
```python
from utils import add_context

context = "Current phase: planning\nSession: abc123"
add_context(context)
```

**JSON output with context:**
```python
import json

output = {
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": "Your context here",
    }
}
print(json.dumps(output))
sys.exit(0)
```

## Modify Tool Input

**PreToolUse input modification:**
```python
import json

output = {
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "updatedInput": {
            "tool_input": {
                "prompt": "Modified prompt here",
            },
        },
    }
}
print(json.dumps(output))
sys.exit(0)
```

## Cache Operations

**Read/write cache:**
```python
from utils import get_cache, set_cache, load_cache, write_cache

# Single value
current_phase = get_cache("current_phase")
set_cache("current_phase", "planning")

# Full cache
cache = load_cache()
cache["my_key"] = "value"
write_cache(cache)
```

## Status Operations

**Read/write project status:**
```python
from utils import get_status, set_status

milestone = get_status("current_milestone")
set_status("current_task", "T-001")
```

## Path Validation

**Check dangerous paths:**
```python
CRITICAL_PATHS = {"/etc/passwd", "/etc/shadow", "/boot/"}

def is_dangerous_path(path: str) -> bool:
    return any(p in path for p in CRITICAL_PATHS)
```

**Safe directory check:**
```python
SAFE_DIRS = {"/.claude/", "/src/", "/tests/"}

def is_safe_path(path: str) -> bool:
    return any(d in path for d in SAFE_DIRS)
```

## Command Validation

**Regex-based command blocking:**
```python
import re

DANGEROUS_PATTERNS = [
    (r"rm\s+-[rf]+\s+/\s*$", "rm -rf /"),
    (r"dd\s+if=/dev/zero", "dd to device"),
]

def check_command(cmd: str) -> str | None:
    for pattern, desc in DANGEROUS_PATTERNS:
        if re.search(pattern, cmd, re.IGNORECASE):
            return f"Blocked: {desc}"
    return None
```

## Phase Guard Pattern

**Block actions by phase:**
```python
from utils import get_cache, block_response

current_phase = get_cache("current_phase")

if current_phase == "explore":
    if is_code_file(file_path):
        block_response("Cannot write code during explore phase")
```

## Error Handling

**Safe input parsing:**
```python
def main() -> None:
    try:
        input_data = read_stdin_json()
        if not input_data:
            sys.exit(0)

        # Hook logic

    except Exception as e:
        print(f"Hook error: {e}", file=sys.stderr)
        sys.exit(0)  # Fail open
```

## Logging

**Log to file:**
```python
from utils import log

log(f"Processing tool: {tool_name}")
log(f"BLOCKED: {reason}")
```

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Success/allow |
| `2` | Block (stderr shown to Claude) |
| Other | Non-blocking error |
