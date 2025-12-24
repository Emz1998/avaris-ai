#!/usr/bin/env python3
"""Validate subagent invocation order in workflow."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import read_stdin_json, get_cache, set_cache


DEFAULT_SUBAGENTS = [
    "codebase-explorer",
    "research-specialist",
    "research-consultant",
    "strategic-planner",
    "plan-consultant",
    "test-manager",
    "code-reviewer",
    "code-specialist",
    "version-manager",
]


def get_validation_messages(next_subagent: str) -> dict[str, str]:
    """Get validation messages for subagent transitions."""
    return {
        "unknown": f"Unknown subagent: {next_subagent}",
        "allow": f"You can proceed to the next subagent: {next_subagent}.",
        "rollback": f"Cannot call back the previous subagent: {next_subagent}.",
        "skip": "Cannot skip subagent(s): ",
    }


def is_next_subagent_valid(
    next_subagent: str,
    all_subagents: list[str] = DEFAULT_SUBAGENTS,
) -> bool:
    """Check if transition to next subagent is valid."""
    current_subagent = get_cache("current_subagent")
    messages = get_validation_messages(next_subagent)

    # Check if subagent is in allowed list
    if next_subagent not in all_subagents:
        print(messages["unknown"], file=sys.stderr)
        return False

    # Allow if nothing triggered yet
    if not current_subagent or current_subagent not in all_subagents:
        print(messages["allow"])
        return True

    current_idx = all_subagents.index(current_subagent)
    next_idx = all_subagents.index(next_subagent)

    # Allow same or next in sequence
    if next_idx in (current_idx, current_idx + 1):
        print(messages["allow"])
        return True

    # Block backwards
    if next_idx < current_idx:
        print(messages["rollback"], file=sys.stderr)
        return False

    # Block skipping
    skipped = all_subagents[current_idx + 1 : next_idx]
    print(messages["skip"] + ", ".join(skipped), file=sys.stderr)
    return False


def validate_subagent_order() -> None:
    """Main subagent order validation."""
    try:
        hook_input = read_stdin_json()
        tool_input = hook_input.get("tool_input", {})

        # Safely extract subagent_type from tool_input
        if not isinstance(tool_input, dict):
            sys.exit(0)

        next_subagent = tool_input.get("subagent_type", "")

        if not next_subagent:
            sys.exit(0)

        if not is_next_subagent_valid(next_subagent):
            sys.exit(2)

        set_cache("current_subagent", next_subagent)
        print(f"Current Subagent set to {next_subagent}")
        sys.exit(0)

    except Exception as e:
        print(f"Subagent validation error: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    validate_subagent_order()
