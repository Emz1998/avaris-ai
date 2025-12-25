#!/usr/bin/env python3
"""
Guardrail hook for test-engineer subagent.

Allows Write/Edit only to test files:
- *.test.ts, *.test.tsx, *.test.js, *.test.jsx
- *.spec.ts, *.spec.tsx, *.spec.js, *.spec.jsx
- Files in __tests__/, tests/, test/ directories
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import (
    read_stdin_json,
    get_cache,
    load_cache,
    write_cache,
    block_response,
)

TARGET_SUBAGENT = "test-engineer"
GUARDRAIL_CACHE_KEY = "test_engineer_guardrail_active"
GUARDED_TOOLS = {"Write", "Edit"}

# Test file patterns
TEST_FILE_PATTERNS = [
    # JS/TS patterns
    r"\.test\.(ts|tsx|js|jsx)$",
    r"\.spec\.(ts|tsx|js|jsx)$",
    # Python patterns
    r"test_.*\.py$",
    r".*_test\.py$",
    r"conftest\.py$",
    # Directory patterns
    r"/__tests__/",
    r"/tests/",
    r"/test/",
    r"^tests/",
    r"^test/",
    r"^__tests__/",
]


def is_guardrail_active() -> bool:
    return get_cache(GUARDRAIL_CACHE_KEY) is True


def activate_guardrail() -> None:
    cache = load_cache()
    cache[GUARDRAIL_CACHE_KEY] = True
    write_cache(cache)


def deactivate_guardrail() -> None:
    cache = load_cache()
    cache[GUARDRAIL_CACHE_KEY] = False
    write_cache(cache)


def is_test_file(file_path: str) -> bool:
    """Check if file path is a test file."""
    for pattern in TEST_FILE_PATTERNS:
        if re.search(pattern, file_path):
            return True
    return False


def handle_task_pretool(input_data: dict) -> None:
    tool_input = input_data.get("tool_input", {})
    subagent_type = tool_input.get("subagent_type", "")
    if subagent_type == TARGET_SUBAGENT:
        activate_guardrail()


def handle_tool_pretool(input_data: dict) -> None:
    if not is_guardrail_active():
        return

    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    if tool_name not in GUARDED_TOOLS:
        return

    file_path = tool_input.get("file_path", "")

    if not is_test_file(file_path):
        block_response(
            f"GUARDRAIL: {tool_name} blocked for {TARGET_SUBAGENT}. "
            f"Only test files allowed (*.test.ts, *.spec.ts, __tests__/, tests/). "
            f"Attempted: {file_path}"
        )


def handle_subagent_stop() -> None:
    if is_guardrail_active():
        deactivate_guardrail()


def main() -> None:
    input_data = read_stdin_json()
    if not input_data:
        sys.exit(0)

    hook_event = input_data.get("hook_event_name", "")
    tool_name = input_data.get("tool_name", "")

    if hook_event == "PreToolUse":
        if tool_name == "Task":
            handle_task_pretool(input_data)
        else:
            handle_tool_pretool(input_data)
    elif hook_event == "SubagentStop":
        handle_subagent_stop()

    sys.exit(0)


if __name__ == "__main__":
    main()
