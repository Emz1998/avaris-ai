#!/usr/bin/env python3
# Status Logger Dispatcher
# PreToolUse hook that routes to appropriate logger based on skill name

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.input import read_stdin_json
from status_logger import task_logger, ac_logger, sc_logger

SKILL_HANDLERS = {
    "log:task": task_logger.process,
    "log:ac": ac_logger.process,
    "log:sc": sc_logger.process,
}


def main() -> None:
    input_data = read_stdin_json()
    if not input_data:
        sys.exit(0)

    # Check if this is a Skill tool call
    tool_name = input_data.get("tool_name", "")
    if tool_name != "Skill":
        sys.exit(0)

    # Get tool_input
    tool_input = input_data.get("tool_input", {})
    skill_name = tool_input.get("skill", "")
    args = tool_input.get("args", "")

    # Route to appropriate handler
    handler = SKILL_HANDLERS.get(skill_name)
    if handler is None:
        sys.exit(0)

    # Process the request
    handler(args)


if __name__ == "__main__":
    main()
