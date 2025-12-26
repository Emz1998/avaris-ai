#!/usr/bin/env python3
"""
Guardrail hook for fullstack-developer subagent.

Blocks Write/Edit to markdown files except README.md.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import (  # type: ignore
    GuardrailConfig,
    GuardrailRunner,
    create_extension_blocker,
)

config = GuardrailConfig(
    target_subagent="fullstack-developer",
    cache_key="fullstack_developer_guardrail_active",
    guarded_tools={"Write", "Edit"},
    path_validator=create_extension_blocker(".md", except_files=["README.md"]),
)

if __name__ == "__main__":
    GuardrailRunner(config).run()
