#!/usr/bin/env python3
"""PreToolUse hook to activate guardrails when /build skill is triggered."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import read_stdin_json, load_cache, write_cache  # type: ignore

# Skills that activate the guardrails
BUILD_SKILLS = {"build", "implement"}
BUILD_SKILL_CACHE_KEY = "build_skill_active"

# Guardrail cache keys to activate when /build is triggered
BUILD_GUARDRAIL_KEYS = [
    "test_engineer_guardrail_active",
    "fullstack_developer_guardrail_active",
    "code_reviewer_guardrail_active",
    "version_manager_guardrail_active",
    "engineer_task_logger_guardrail_active",
]


def activate_build_guardrails() -> None:
    """Activate build skill and all related guardrails in cache."""
    cache = load_cache()
    cache[BUILD_SKILL_CACHE_KEY] = True
    for key in BUILD_GUARDRAIL_KEYS:
        cache[key] = True
    write_cache(cache)


def main() -> None:
    """Check if /build skill is triggered and activate guardrails."""
    input_data = read_stdin_json()
    if not input_data:
        sys.exit(0)

    tool_input = input_data.get("tool_input", {})
    skill_name = tool_input.get("skill", "")

    if skill_name in BUILD_SKILLS:
        activate_build_guardrails()

    sys.exit(0)


if __name__ == "__main__":
    main()
