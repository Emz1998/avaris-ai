#!/usr/bin/env python3
"""
Guardrail hook for version-manager subagent.

Blocks:
- Write, Edit, MultiEdit tools
- Bash commands outside safe git operations
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import (  # type: ignore
    GuardrailConfig,
    GuardrailRunner,
)

config = GuardrailConfig(
    target_subagent="version-manager",
    cache_key="version_manager_guardrail_active",
    blocked_tools={"Write", "Edit", "MultiEdit"},
    block_unsafe_bash=True,
)

if __name__ == "__main__":
    GuardrailRunner(config).run()
