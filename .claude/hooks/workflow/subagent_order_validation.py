#!/usr/bin/env python3
"""Validate subagent invocation based on current phase."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import read_stdin_json, get_cache, set_cache


# Phase to allowed subagents mapping
PHASE_SUBAGENTS = {
    "explore": ["codebase-explorer"],
    "research": ["research-specialist", "research-consultant"],
    "plan": ["planning-specialist"],
    "plan:consult": ["plan-consultant"],
    "code": ["test-engineer", "version-manager", "fullstack-developer", "code-reviewer", "version-manager"],
    "commit": ["version-manager"],
}

# Ordered phases - subagents must be triggered in sequence
ORDERED_PHASES = ["code"]


def get_allowed_subagents(phase: str) -> list[str]:
    """Get list of allowed subagents for a phase (unique values)."""
    return list(set(PHASE_SUBAGENTS.get(phase, [])))


def get_phase_sequence(phase: str) -> list[str]:
    """Get the ordered sequence for a phase."""
    return PHASE_SUBAGENTS.get(phase, [])


def get_all_known_subagents() -> list[str]:
    """Get all known subagents across all phases."""
    all_subagents = []
    for subagents in PHASE_SUBAGENTS.values():
        all_subagents.extend(subagents)
    return list(set(all_subagents))


def is_subagent_allowed_for_phase(subagent: str, phase: str) -> bool:
    """Check if subagent is allowed for the current phase."""
    allowed = get_allowed_subagents(phase)
    return subagent in allowed


def validate_ordered_phase(subagent: str, phase: str) -> tuple[bool, str]:
    """Validate subagent order within an ordered phase using position tracking."""
    sequence = get_phase_sequence(phase)
    current_position = get_cache("code_phase_position") or 0

    # Check if subagent matches expected position
    if current_position >= len(sequence):
        return False, f"Phase '{phase}' sequence already completed"

    expected = sequence[current_position]

    # Allow retry of current position
    if current_position > 0 and subagent == sequence[current_position - 1]:
        return True, f"Retrying '{subagent}' at position {current_position}"

    # Check if subagent matches expected
    if subagent == expected:
        set_cache("code_phase_position", current_position + 1)
        return True, f"Proceeding to '{subagent}' (step {current_position + 1}/{len(sequence)})"

    return False, f"Expected '{expected}' at step {current_position + 1}, got '{subagent}'"


def validate_subagent_by_phase() -> None:
    """Main subagent phase validation."""
    try:
        hook_input = read_stdin_json()
        tool_input = hook_input.get("tool_input", {})

        # Safely extract subagent_type from tool_input
        if not isinstance(tool_input, dict):
            sys.exit(0)

        next_subagent = tool_input.get("subagent_type", "")

        if not next_subagent:
            sys.exit(0)

        # Get current phase from cache
        current_phase = get_cache("current_phase")

        if not current_phase:
            print("No phase set. Allowing subagent.", file=sys.stderr)
            sys.exit(0)

        # Check if subagent is known
        all_known = get_all_known_subagents()
        if next_subagent not in all_known:
            print(f"Unknown subagent: {next_subagent}. Allowing.", file=sys.stderr)
            sys.exit(0)

        # Validate subagent against current phase
        if not is_subagent_allowed_for_phase(next_subagent, current_phase):
            allowed = get_allowed_subagents(current_phase)
            allowed_str = ", ".join(allowed) if allowed else "none"
            print(
                f"Subagent '{next_subagent}' not allowed in phase '{current_phase}'. "
                f"Allowed: {allowed_str}",
                file=sys.stderr,
            )
            sys.exit(2)

        # For ordered phases, validate sequence
        if current_phase in ORDERED_PHASES:
            is_valid, message = validate_ordered_phase(next_subagent, current_phase)
            if not is_valid:
                print(message, file=sys.stderr)
                sys.exit(2)
            print(message)
        else:
            print(f"Subagent '{next_subagent}' allowed for phase '{current_phase}'")

        # Update current subagent in cache
        set_cache("current_subagent", next_subagent)
        sys.exit(0)

    except Exception as e:
        print(f"Subagent validation error: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    validate_subagent_by_phase()
