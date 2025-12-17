#!/usr/bin/env python3
"""
PreToolUse hook for Task tool interception.
Intercepts subagent invocations and injects prompt refinement instructions.
"""
import json
import sys
from pathlib import Path
import subprocess

# Add parent directory to path for utils imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import read_stdin_json  # type: ignore


def main() -> None:
    # hook_input = read_stdin_json()
    hook_input = read_stdin_json()
    print("working")

    initial_prompt = hook_input.get("prompt", "")

    # Skip if missing required fields
    if not initial_prompt.startswith("--"):
        sys.exit(0)

    # Parse the prompt
    parsed_prompt = initial_prompt.replace("--", "").strip()

    # Build the refinement prompt
    prompt = f"/prompt {parsed_prompt}"

    claude_output = subprocess.run(
        [
            "claude",
            "-p",
            prompt,
            "--model",
            "haiku",
            "--tools",
            "Read",
        ],
        capture_output=True,
        text=True,
    )
    # Output JSON with additionalContext for PostToolUse-style injection
    if "---" not in claude_output.stdout:
        output = claude_output.stdout
    else:
        output = claude_output.stdout.split("---")[1].strip()
    print(output)
    sys.exit(0)


if __name__ == "__main__":
    main()
