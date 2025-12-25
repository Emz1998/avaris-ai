#!/usr/bin/env python3
"""
Guardrail hook for project-manager subagent.

Allows:
- Skill with skill names: "log:ac", "log:sc", "log:task"

Blocks:
- All Write/Edit operations
- All other Skill operations
"""
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

TARGET_SUBAGENT = "project-manager"
GUARDRAIL_CACHE_KEY = "project_manager_guardrail_active"
BLOCKED_TOOLS = {"Write", "Edit"}
ALLOWED_SKILLS = {"log:ac", "log:sc", "log:task"}


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

    # Block Write/Edit tools entirely
    if tool_name in BLOCKED_TOOLS:
        block_response(
            f"GUARDRAIL: {tool_name} blocked for {TARGET_SUBAGENT}. "
            "No file writing allowed."
        )

    # Handle Skill tool
    if tool_name == "Skill":
        skill_name = tool_input.get("skill", "")
        if skill_name not in ALLOWED_SKILLS:
            block_response(
                f"GUARDRAIL: Skill blocked for {TARGET_SUBAGENT}. "
                f"Only {ALLOWED_SKILLS} allowed. Attempted: {skill_name}"
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
