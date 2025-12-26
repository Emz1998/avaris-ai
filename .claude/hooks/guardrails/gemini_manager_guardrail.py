#!/usr/bin/env python3
"""
Guardrail hook for gemini-manager subagent.

Allows:
- Write/Edit to: project/{version}/phases/milestones/{milestone}/decisions/
- Skill with skill name "discuss:gemini"

Blocks all other Write/Edit/Skill operations.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import (  # type: ignore
    GuardrailConfig,
    GuardrailRunner,
    create_directory_validator,
)

config = GuardrailConfig(
    target_subagent="gemini-manager",
    cache_key="gemini_manager_guardrail_active",
    guarded_tools={"Write", "Edit"},
    blocked_skills_except={"discuss:gemini"},
    path_validator=create_directory_validator("decisions"),
)

if __name__ == "__main__":
    GuardrailRunner(config).run()
