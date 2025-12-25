#!/usr/bin/env python3
"""Context injector hook - Injects roadmap context into Claude sessions."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import add_context, read_stdin_json, set_status
from utils.roadmap import (
    get_current_version,
    get_roadmap_path,
    load_roadmap,
)


def get_current_context(roadmap: dict) -> dict:
    """Extract current phase, milestone, and task from roadmap."""
    current = roadmap.get("current", {})
    phase_id = current.get("phase")
    milestone_id = current.get("milestone")
    task_id = current.get("task")

    phase_data = None
    milestone_data = None
    task_data = None

    # Find current phase
    for phase in roadmap.get("phases", []):
        if phase.get("id") == phase_id:
            phase_data = phase
            # Find current milestone
            for milestone in phase.get("milestones", []):
                if milestone.get("id") == milestone_id:
                    milestone_data = milestone
                    # Find current task
                    for task in milestone.get("tasks", []):
                        if task.get("id") == task_id:
                            task_data = task
                            break
                    break
            break

    return {
        "phase": phase_data,
        "milestone": milestone_data,
        "task": task_data,
    }


def format_acceptance_criteria(task: dict | None) -> str:
    """Format task acceptance criteria as a string."""
    if not task:
        return "N/A"

    acs = task.get("acceptance_criteria", [])
    if not acs:
        return "None defined"

    lines = []
    for ac in acs:
        id_ref = ac.get("id_reference", "Unknown")
        status = ac.get("status", "unknown")
        lines.append(f"  - {id_ref}: {status}")
    return "\n" + "\n".join(lines) if lines else "None defined"


def format_success_criteria(milestone: dict | None) -> str:
    """Format milestone success criteria as a string."""
    if not milestone:
        return "N/A"

    scs = milestone.get("success_criteria", [])
    if not scs:
        return "None defined"

    lines = []
    for sc in scs:
        id_ref = sc.get("id_reference", "Unknown")
        status = sc.get("status", "unknown")
        lines.append(f"  - {id_ref}: {status}")
    return "\n" + "\n".join(lines) if lines else "None defined"


def format_summary(summary: dict) -> str:
    """Format roadmap summary as a string."""
    phases = summary.get("phases", {})
    milestones = summary.get("milestones", {})
    tasks = summary.get("tasks", {})

    return f"""
  Phases: {phases.get('completed', 0)}/{phases.get('total', 0)} completed
  Milestones: {milestones.get('completed', 0)}/{milestones.get('total', 0)} completed
  Tasks: {tasks.get('completed', 0)}/{tasks.get('total', 0)} completed"""


def inject_context() -> None:
    """Inject roadmap context into the session."""
    input_data = read_stdin_json()
    session_id = input_data.get("session_id", "unknown")

    # Set the session id in status
    set_status("current_session_id", session_id)

    # Load roadmap
    version = get_current_version()
    if not version:
        add_context(f"Session ID: {session_id}\nRoadmap: Not available (no version)")
        return

    roadmap_path = get_roadmap_path(version)
    roadmap = load_roadmap(roadmap_path)
    if not roadmap:
        add_context(f"Session ID: {session_id}\nRoadmap: Not found at {roadmap_path}")
        return

    # Get current context
    current_ctx = get_current_context(roadmap)
    phase = current_ctx["phase"]
    milestone = current_ctx["milestone"]
    task = current_ctx["task"]
    summary = roadmap.get("summary", {})

    # Build context string
    context = f"""
Session ID: {session_id}

Current Phase: {phase.get('id', 'N/A') if phase else 'N/A'} - {phase.get('name', 'N/A') if phase else 'N/A'}
Current Milestone: {milestone.get('id', 'N/A') if milestone else 'N/A'} - {milestone.get('name', 'N/A') if milestone else 'N/A'}
Current Task: {task.get('id', 'N/A') if task else 'N/A'} - {task.get('description', 'N/A') if task else 'N/A'}

Task Acceptance Criteria:{format_acceptance_criteria(task)}

Milestone Success Criteria:{format_success_criteria(milestone)}

Summary:{format_summary(summary)}
"""

    add_context(context.strip())


if __name__ == "__main__":
    inject_context()
