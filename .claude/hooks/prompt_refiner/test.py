#!/usr/bin/env python3
"""
PreToolUse hook for Task tool interception.
Intercepts subagent invocations and injects prompt refinement instructions.
"""

import sys
import subprocess
import json


def main() -> None:
    initial_prompt = "--prompt Plan about the best way to create a blog website"
    parsed_prompt = initial_prompt.replace("--prompt", "").strip()
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
    if "---" not in claude_output.stdout:
        output = claude_output.stdout
    else:
        output = claude_output.stdout.split("---")[1].strip()

    print(output)
    sys.exit(0)


if __name__ == "__main__":
    main()
