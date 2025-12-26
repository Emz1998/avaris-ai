#!/usr/bin/env python3
"""
Guardrail hook for plan-consultant subagent.

Only allows Write/Edit to:
project/{version}/phases/milestones/{milestone}/decisions/
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
    target_subagent="plan-consultant",
    cache_key="plan_consultant_guardrail_active",
    guarded_tools={"Write", "Edit"},
    path_validator=create_directory_validator("decisions"),
)

if __name__ == "__main__":
    GuardrailRunner(config).run()
