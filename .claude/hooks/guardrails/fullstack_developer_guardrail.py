#!/usr/bin/env python3
"""
Guardrail hook for fullstack-developer subagent.

Blocks Write/Edit to markdown files except README.md.
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

TARGET_SUBAGENT = "fullstack-developer"
GUARDRAIL_CACHE_KEY = "fullstack_developer_guardrail_active"
GUARDED_TOOLS = {"Write", "Edit"}


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


def is_blocked_markdown(file_path: str) -> bool:
    """Check if file is a blocked markdown file (any .md except README.md)."""
    if not file_path.endswith(".md"):
        return False
    filename = Path(file_path).name
    return filename.lower() != "readme.md"


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

    if is_blocked_markdown(file_path):
        block_response(
            f"GUARDRAIL: {tool_name} blocked for {TARGET_SUBAGENT}. "
            f"Markdown files blocked except README.md. Attempted: {file_path}"
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
