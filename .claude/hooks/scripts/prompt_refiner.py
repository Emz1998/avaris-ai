#!/usr/bin/env python3
"""
PreToolUse hook for Task tool interception.
Intercepts subagent invocations and injects prompt refinement instructions.
"""
import json
import sys
from pathlib import Path

# Add parent directory to path for utils imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.input import read_stdin_json, get_cache, set_cache


def main() -> None:
    hook_input = read_stdin_json()
    print(hook_input)

    # Only process Task tool invocations
    tool_name = hook_input.get("tool_name", "")
    if tool_name != "Task":
        sys.exit(0)

    tool_input = hook_input.get("tool_input", {})
    initial_prompt = tool_input.get("prompt", "")
    initial_agent = tool_input.get("subagent_type", "")

    retrigger_flag = get_cache("retrigger_flag")
    set_cache("retrigger_flag", retrigger_flag + 1)

    # Skip if missing required fields
    if not initial_prompt or not initial_agent:
        sys.exit(0)

    # Skip prompt refinement for the refinement agents themselves to avoid infinite loop
    skip_agents = ["prompt-engineer", "prompt-reviewer"]
    if initial_agent in skip_agents:
        sys.exit(0)

    # Build the refinement instruction
    refinement_instruction = f"""
**Prompt Quality Check Required**

Check if {initial_prompt} meets the following criteria:

- Are intructions, examples, output style, tool usage intent, success criteria defined?
- Is the prompt clear and concise?
- Is the request explicit enough? (not relying on implied intent)
- Is the "why" or context included?
- Do examples align with desired behavior?
- Is the format/output style specified?
- Is tool usage intent clear? (suggest vs. implement)
- Are instructions framed positively? (what to do, not what to avoid)
- Does prompt style match desired output style?
- Is verbosity level specified?
- For multi-step tasks, is state tracking considered?
- Are success criteria defined?

If the prompt does not meet the criteria, refine the prompt using the following workflow:

1. **Call `agent-prompt-engineer`** to review and refine this prompt:
   <subagent_prompt>
   {initial_prompt}
   </subagent_prompt>

2. **Call `agent-prompt-reviewer`** to rate the refined prompt (scale 1-10)

3. **Iteration Loop:**
   - If rating < 9: Re-invoke `agent-prompt-engineer` with feedback
   - Repeat until rating >= 9

4. **Execute Original Agent:**
   - Once quality check passes, invoke `{initial_agent}` with the refined prompt

*Target Agent:* `{initial_agent}`
*Original Prompt Length:* {len(initial_prompt)} characters
"""

    # Output JSON with additionalContext for PostToolUse-style injection
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": "Prompt quality check required",
            "additionalContext": refinement_instruction.strip(),
        }
    }

    print(json.dumps(output), file=sys.stderr)
    sys.exit(2) if retrigger_flag == 0 else sys.exit(0)


if __name__ == "__main__":
    main()
