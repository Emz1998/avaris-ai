#!/usr/bin/env python3
"""
Guardrail hook for codebase-explorer subagent.

Only allows Write/Edit to:
project/{version}/phases/milestones/{milestone}/codebase-status/codebase-status_{yyyy-mm-dd}_{session_id}.md
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
    target_subagent="codebase-explorer",
    cache_key="codebase_explorer_guardrail_active",
    guarded_tools={"Write", "Edit"},
    path_validator=create_session_file_validator("codebase-status", "codebase-status"),
)

if __name__ == "__main__":
    GuardrailRunner(config).run()
