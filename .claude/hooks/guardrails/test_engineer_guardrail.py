#!/usr/bin/env python3
"""
Guardrail hook for test-engineer subagent.

Allows Write/Edit only to test files:
- *.test.ts, *.test.tsx, *.test.js, *.test.jsx
- *.spec.ts, *.spec.tsx, *.spec.js, *.spec.jsx
- Files in __tests__/, tests/, test/ directories
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import (  # type: ignore
    GuardrailConfig,
    GuardrailRunner,
    create_pattern_validator,
)

TEST_FILE_PATTERNS = [
    r"\.test\.(ts|tsx|js|jsx)$",
    r"\.spec\.(ts|tsx|js|jsx)$",
    r"test_.*\.py$",
    r".*_test\.py$",
    r"conftest\.py$",
    r"/__tests__/",
    r"/tests/",
    r"/test/",
    r"^tests/",
    r"^test/",
    r"^__tests__/",
]

config = GuardrailConfig(
    target_subagent="test-engineer",
    cache_key="test_engineer_guardrail_active",
    guarded_tools={"Write", "Edit"},
    path_validator=create_pattern_validator(
        TEST_FILE_PATTERNS,
        allow_match=True,
        error_msg="Only test files allowed (*.test.ts, *.spec.ts, __tests__/, tests/)",
    ),
)

if __name__ == "__main__":
    GuardrailRunner(config).run()
