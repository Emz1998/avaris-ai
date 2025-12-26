#!/usr/bin/env python3
"""
Guardrail hook for project-manager subagent.

Allows:
- Skill with skill names: "log:ac", "log:sc", "log:task"

Blocks:
- All Write/Edit operations
- All other Skill operations
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import (  # type: ignore
    GuardrailConfig,
    GuardrailRunner,
)

config = GuardrailConfig(
    target_subagent="project-manager",
    cache_key="project_manager_guardrail_active",
    blocked_tools={"Write", "Edit"},
    allowed_skills={"log:ac", "log:sc", "log:task"},
)

if __name__ == "__main__":
    GuardrailRunner(config).run()
