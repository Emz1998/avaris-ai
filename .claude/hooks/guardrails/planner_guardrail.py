#!/usr/bin/env python3
"""
Guardrail hook for planning-specialist subagent.

Only allows Write/Edit to:
project/{version}/phases/milestones/{milestone}/plans/plan_{yyyy-mm-dd}_{session_id}.md
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import (  # type: ignore
    GuardrailConfig,
    GuardrailRunner,
    create_session_file_validator,
)

config = GuardrailConfig(
    target_subagent="planning-specialist",
    cache_key="planner_guardrail_active",
    guarded_tools={"Write", "Edit"},
    path_validator=create_session_file_validator("plans", "plan"),
)

if __name__ == "__main__":
    GuardrailRunner(config).run()
