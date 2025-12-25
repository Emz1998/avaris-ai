#!/usr/bin/env python3
"""PreToolUse hook to activate stop guard when /build skill is triggered."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import read_stdin_json, load_cache, write_cache

# Skills that activate the stop guard
STOP_GUARD_SKILLS = {"build", "implement"}
BUILD_SKILL_CACHE_KEY = "build_skill_active"


def activate_build_skill() -> None:
    """Activate build skill tracking in cache."""
    cache = load_cache()
    cache[BUILD_SKILL_CACHE_KEY] = True
    write_cache(cache)


def main() -> None:
    """Check if /build skill is triggered and activate stop guard."""
    input_data = read_stdin_json()
    if not input_data:
        sys.exit(0)

    tool_input = input_data.get("tool_input", {})
    skill_name = tool_input.get("skill", "")

    if skill_name in STOP_GUARD_SKILLS:
        activate_build_skill()

    sys.exit(0)


if __name__ == "__main__":
    main()
