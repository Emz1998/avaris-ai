#!/usr/bin/env python3
"""Inject context into hook output for implement workflow."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import add_context, get_status, read_stdin_json, set_status


def build_context_string(session_id: str) -> str:
    """Build context string from project status."""
    status_keys = [
        ("current_milestone", "Current Milestone"),
        ("last_milestone_completed", "Last Milestone Completed"),
        ("last_task_completed", "Last Task Completed"),
        ("tasks_remaining", "Remaining Tasks"),
        ("milestones_remaining", "Remaining Milestones"),
        ("total_tasks", "Total Tasks"),
        ("total_milestones", "Total Milestones"),
        ("total_phases", "Total Phases"),
        ("target_release_date", "Target Release Date"),
        ("current_phase", "Current Phase"),
        ("milestones_completed", "Milestones Completed"),
        ("tasks_completed", "Tasks Completed"),
    ]

    lines = [f"Session ID: {session_id}"]
    for key, label in status_keys:
        value = get_status(key)
        lines.append(f"{label}: {value}")

    return "\n".join(lines)


def inject_context() -> None:
    """Inject workflow context into session."""
    try:
        hook_input = read_stdin_json()
        session_id = hook_input.get("session_id", "")

        # Store session id in status
        if session_id:
            set_status("current_session_id", session_id)

        context = build_context_string(session_id)
        add_context(context)

    except Exception as e:
        print(f"Context injection error: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    inject_context()
