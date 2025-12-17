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

from utils.input import read_stdin_json  # type: ignore


def main() -> None:
    hook_input = read_stdin_json()

    # Only process Task tool invocations
    tool_name = hook_input.get("tool_name", "")
    if tool_name != "Task":
        sys.exit(0)

    tool_input = hook_input.get("tool_input", {})
    initial_prompt = tool_input.get("prompt", "")
    initial_agent = tool_input.get("subagent_type", "")

    Path("initial_prompt.log").write_text(str(initial_prompt))

    # Skip if missing required fields
    if not initial_prompt or not initial_agent:
        sys.exit(0)

    # Build the refinement instruction
    refinement_instruction = f"""Add additional context to the following prompt to make 
    it more clear and concise: 
    
    {initial_prompt}
    
    Do not rewrite the initial prompt, only add additional context.
    """

    # Run the claude headless command

    claude_output = subprocess.run(
        [
            "claude",
            "-p",
            refinement_instruction,
            "--model",
            "haiku",
            "--tools",
            "Read",
        ],
        capture_output=True,
        text=True,
    )

    Path("refined_prompt.log").write_text(str(claude_output.stdout))
    # Output JSON with additionalContext for PostToolUse-style injection
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "updatedInput": {
                "tool_input": {
                    "prompt": claude_output.stdout.strip(),
                },
            },
        }
    }

    print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()
