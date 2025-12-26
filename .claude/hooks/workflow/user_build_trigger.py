#!/usr/bin/env python3
"""UserPromptSubmit hook to activate stop guard when user types /build command."""

import sys
import re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import read_stdin_json, load_cache, write_cache  # type: ignore

# Command patterns that activate the stop guard
BUILD_COMMANDS = {"/build", "/implement"}
BUILD_SKILL_CACHE_KEY = "build_skill_active"


def activate_build_skill() -> None:
    """Activate build skill in cache."""
    cache = load_cache()
    cache[BUILD_SKILL_CACHE_KEY] = True
    write_cache(cache)


def extract_command(prompt: str) -> str | None:
    """Extract slash command from user prompt."""
    prompt_stripped = prompt.strip()
    # Match /command at start of prompt
    match = re.match(r"^(/\w+)", prompt_stripped)
    if match:
        return match.group(1).lower()
    return None


def main() -> None:
    """Check if user typed /build command and activate stop guard."""
    input_data = read_stdin_json()
    if not input_data:
        sys.exit(0)

    hook_event = input_data.get("hook_event_name", "")
    if hook_event != "UserPromptSubmit":
        sys.exit(0)

    prompt = input_data.get("prompt", "")
    if not prompt:
        sys.exit(0)

    command = extract_command(prompt)
    if command and command in BUILD_COMMANDS:
        activate_build_skill()

    sys.exit(0)


if __name__ == "__main__":
    main()
