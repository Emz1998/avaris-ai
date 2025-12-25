#!/usr/bin/env python3
"""
Guardrail hook for version-manager subagent.

This hook operates across multiple events:
- PreToolUse (Task matcher): Detects version-manager subagent start, activates guardrail
- PreToolUse (Write|Edit|MultiEdit|Bash): Validates tool use during active guardrail
- SubagentStop: Detects subagent completion, deactivates guardrail

Blocks during active guardrail:
- Write, Edit, MultiEdit tools
- Bash commands outside safe git operations
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import (
    read_stdin_json,
    get_cache,
    load_cache,
    write_cache,
    block_tool,
    block_unsafe_bash,
)

# Target subagent this guardrail applies to
TARGET_SUBAGENT = "version-manager"

# Cache key for guardrail state
GUARDRAIL_CACHE_KEY = "version_manager_guardrail_active"

# Tools that are completely blocked during guardrail
BLOCKED_TOOLS = {"Write", "Edit", "MultiEdit"}


def is_guardrail_active() -> bool:
    """Check if version-manager guardrail is currently active."""
    return get_cache(GUARDRAIL_CACHE_KEY) is True


def activate_guardrail() -> None:
    """Activate the version-manager guardrail in cache."""
    cache = load_cache()
    cache[GUARDRAIL_CACHE_KEY] = True
    write_cache(cache)


def deactivate_guardrail() -> None:
    """Deactivate the version-manager guardrail in cache."""
    cache = load_cache()
    cache[GUARDRAIL_CACHE_KEY] = False
    write_cache(cache)


def handle_task_pretool(input_data: dict) -> None:
    """
    Handle PreToolUse for Task tool.
    Detects version-manager subagent start and activates guardrail.
    """
    tool_input = input_data.get("tool_input", {})
    subagent_type = tool_input.get("subagent_type", "")

    if subagent_type == TARGET_SUBAGENT:
        activate_guardrail()


def handle_tool_pretool(input_data: dict) -> None:
    """
    Handle PreToolUse for Write|Edit|MultiEdit|Bash tools.
    Validates tool use if guardrail is active.
    """
    if not is_guardrail_active():
        return

    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    # Block Write/Edit/MultiEdit tools entirely
    block_tool(
        tool_name,
        BLOCKED_TOOLS,
        f"GUARDRAIL: {tool_name} tool is blocked for version-manager subagent. "
        "This subagent is restricted to git operations only.",
    )

    # For Bash, only allow safe git commands
    if tool_name == "Bash":
        command = tool_input.get("command", "")
        block_unsafe_bash(
            command,
            f"GUARDRAIL: Bash command blocked for version-manager subagent. "
            f"Only safe git commands are allowed. Attempted: {command[:100]}",
        )


def handle_subagent_stop() -> None:
    """
    Handle SubagentStop event.
    Deactivates guardrail when version-manager subagent completes.
    """
    if is_guardrail_active():
        deactivate_guardrail()


def main() -> None:
    """Entry point for the hook."""
    input_data = read_stdin_json()
    if not input_data:
        sys.exit(0)

    hook_event = input_data.get("hook_event_name", "")
    tool_name = input_data.get("tool_name", "")

    # Route to appropriate handler based on event type
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
