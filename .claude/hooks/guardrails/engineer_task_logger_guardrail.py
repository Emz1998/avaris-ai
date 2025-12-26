#!/usr/bin/env python3
# Engineer Task Logger Guardrail
# Blocks implementation tools until task is logged as "in_progress"

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import (  # type: ignore
    GuardrailConfig,
    GuardrailRunner,
    block_response,
    get_cache,
    load_cache,
    write_cache,
)

ENGINEER_AGENTS = {
    "backend-engineer",
    "frontend-engineer",
    "fullstack-developer",
    "html-prototyper",
    "react-prototyper",
    "test-engineer",
}


class EngineerTaskLoggerRunner(GuardrailRunner):
    """Extended runner that requires task logging before implementation."""

    def __init__(self, config: GuardrailConfig):
        super().__init__(config)
        self.task_logged_key = "engineer_task_logged"

    def is_task_logged(self) -> bool:
        return get_cache(self.task_logged_key) is True

    def set_task_logged(self, value: bool) -> None:
        cache = load_cache()
        cache[self.task_logged_key] = value
        write_cache(cache)

    def activate(self) -> None:
        super().activate()
        self.set_task_logged(False)

    def deactivate(self) -> None:
        super().deactivate()
        self.set_task_logged(False)

    def handle_task_pretool(self, input_data: dict) -> None:
        """Activate guardrail when any engineer subagent is spawned."""
        tool_input = input_data.get("tool_input", {})
        subagent_type = tool_input.get("subagent_type", "")
        if subagent_type in ENGINEER_AGENTS:
            self.activate()

    def handle_tool_pretool(self, input_data: dict) -> None:
        if not self.is_active():
            return

        tool_name = input_data.get("tool_name", "")
        tool_input = input_data.get("tool_input", {})

        # Check for log:task with in_progress - allow and mark logged
        if tool_name == "Skill":
            skill_name = tool_input.get("skill", "")
            args = tool_input.get("args", "")
            if skill_name == "log:task" and "in_progress" in args:
                self.set_task_logged(True)
            return

        # Block ALL tools if task not logged
        if not self.is_task_logged():
            block_response(
                f"GUARDRAIL: {tool_name} blocked. "
                "Engineer subagents must log task as 'in_progress' before any tool use. "
                "Use: /log:task <task-id> in_progress"
            )


config = GuardrailConfig(
    target_subagent="engineer-agents",
    cache_key="engineer_task_logger_guardrail_active",
)

if __name__ == "__main__":
    EngineerTaskLoggerRunner(config).run()
