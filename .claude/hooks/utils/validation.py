"""Format validation utilities."""

import re

PATTERNS = {
    "milestone": r"MS-(\d{3})",
    "milestone_strict": r"^MS-\d{3}$",
    "task_strict": r"^T\d{3}$",
    "ac_strict": r"^AC-\d{3}$",
    "sc_strict": r"^SC-\d{3}$",
}


class InvalidFormatError(Exception):
    """Raised when format is invalid."""

    pass


def validate_format(value: str, pattern: str, entity_name: str, example: str) -> None:
    """Generic format validator."""
    if not re.match(pattern, value):
        raise InvalidFormatError(
            f"Invalid {entity_name} format: '{value}'. Expected: {example}"
        )


def validate_milestone(milestone: str) -> None:
    """Validate milestone format (MS-XXX)."""
    validate_format(
        milestone, PATTERNS["milestone_strict"], "milestone", "MS-XXX (e.g., MS-001)"
    )


def validate_task(task: str) -> None:
    """Validate task format (TXXX)."""
    validate_format(task, PATTERNS["task_strict"], "task", "TXXX (e.g., T001)")


def validate_ac(ac_id: str) -> None:
    """Validate acceptance criteria format (AC-XXX)."""
    validate_format(ac_id, PATTERNS["ac_strict"], "AC ID", "AC-XXX (e.g., AC-001)")


def validate_sc(sc_id: str) -> None:
    """Validate success criteria format (SC-XXX)."""
    validate_format(sc_id, PATTERNS["sc_strict"], "SC ID", "SC-XXX (e.g., SC-001)")
