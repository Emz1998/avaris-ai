#!/usr/bin/env python3
# Auto Resolver for Milestones and Phases
# Automatically resolves milestones when all tasks are completed,
# and phases when all milestones are completed.

import json
import os
from datetime import datetime, timezone
from pathlib import Path


def get_project_dir() -> Path:
    """Get project directory from environment or cwd."""
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
    return Path(project_dir)


def get_current_version() -> str:
    """Retrieve current_version from product.json."""
    project_dir = get_project_dir()
    product_path = project_dir / "project" / "product.json"

    if not product_path.exists():
        return ""

    try:
        with open(product_path, "r") as f:
            product = json.load(f)
        return product.get("current_version", "")
    except (json.JSONDecodeError, IOError):
        return ""


def get_roadmap_path(version: str) -> Path:
    """Get roadmap.json path for the given version."""
    project_dir = get_project_dir()
    return project_dir / "project" / version / "release-plan" / "roadmap.json"


def load_roadmap(roadmap_path: Path) -> dict | None:
    """Load roadmap.json file."""
    if not roadmap_path.exists():
        return None

    try:
        with open(roadmap_path, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None


def save_roadmap(roadmap_path: Path, roadmap: dict) -> bool:
    """Save roadmap.json file."""
    try:
        roadmap["metadata"]["last_updated"] = datetime.now(timezone.utc).isoformat()
        with open(roadmap_path, "w") as f:
            json.dump(roadmap, f, indent=2)
        return True
    except IOError:
        return False


def all_tasks_completed(milestone: dict) -> bool:
    """Check if all tasks in a milestone are completed."""
    tasks = milestone.get("tasks", [])
    if not tasks:
        return False
    return all(task.get("status") == "completed" for task in tasks)


def all_milestones_completed(phase: dict) -> bool:
    """Check if all milestones in a phase are completed."""
    milestones = phase.get("milestones", [])
    if not milestones:
        return False
    return all(ms.get("status") == "completed" for ms in milestones)


def resolve_milestones_and_phases(roadmap: dict) -> list[str]:
    """
    Auto-resolve milestones and phases based on their children's status.
    Also reverts completed status if children are no longer all completed.
    Returns list of resolution messages.
    """
    resolutions = []
    phases = roadmap.get("phases", [])

    for phase in phases:
        milestones = phase.get("milestones", [])

        # Check each milestone for completion or reversion
        for milestone in milestones:
            current_status = milestone.get("status")
            tasks_completed = all_tasks_completed(milestone)

            if current_status != "completed" and tasks_completed:
                milestone["status"] = "completed"
                resolutions.append(f"Milestone '{milestone.get('id')}' auto-resolved to 'completed'")
            elif current_status == "completed" and not tasks_completed:
                milestone["status"] = "in_progress"
                resolutions.append(f"Milestone '{milestone.get('id')}' reverted to 'in_progress'")

        # Check the phase for completion or reversion
        current_phase_status = phase.get("status")
        milestones_completed = all_milestones_completed(phase)

        if current_phase_status != "completed" and milestones_completed:
            phase["status"] = "completed"
            resolutions.append(f"Phase '{phase.get('id')}' auto-resolved to 'completed'")
        elif current_phase_status == "completed" and not milestones_completed:
            phase["status"] = "in_progress"
            resolutions.append(f"Phase '{phase.get('id')}' reverted to 'in_progress'")

    return resolutions


def update_current(roadmap: dict) -> str | None:
    """
    Update the 'current' section to point to the next pending task.
    Returns a message if current was updated, None otherwise.
    """
    phases = roadmap.get("phases", [])
    current = roadmap.get("current", {})
    old_current = (current.get("phase"), current.get("milestone"), current.get("task"))

    # Find first non-completed phase, milestone, and task
    new_phase_id = None
    new_milestone_id = None
    new_task_id = None

    for phase in phases:
        if phase.get("status") == "completed":
            continue

        new_phase_id = phase.get("id")
        milestones = phase.get("milestones", [])

        for milestone in milestones:
            if milestone.get("status") == "completed":
                continue

            new_milestone_id = milestone.get("id")
            tasks = milestone.get("tasks", [])

            for task in tasks:
                if task.get("status") == "completed":
                    continue

                new_task_id = task.get("id")
                break

            if new_task_id:
                break

        if new_milestone_id:
            break

    # If all completed, keep pointing to the last items
    if not new_phase_id and phases:
        last_phase = phases[-1]
        new_phase_id = last_phase.get("id")
        milestones = last_phase.get("milestones", [])
        if milestones:
            last_milestone = milestones[-1]
            new_milestone_id = last_milestone.get("id")
            tasks = last_milestone.get("tasks", [])
            if tasks:
                new_task_id = tasks[-1].get("id")

    new_current = (new_phase_id, new_milestone_id, new_task_id)

    if new_current != old_current:
        roadmap["current"] = {
            "phase": new_phase_id,
            "milestone": new_milestone_id,
            "task": new_task_id
        }
        return f"Current updated: phase={new_phase_id}, milestone={new_milestone_id}, task={new_task_id}"

    return None


def update_summary(roadmap: dict) -> None:
    """Update the summary section with current counts."""
    phases = roadmap.get("phases", [])
    summary = roadmap.get("summary", {})

    phase_total = len(phases)
    phase_completed = sum(1 for p in phases if p.get("status") == "completed")

    milestone_total = 0
    milestone_completed = 0
    task_total = 0
    task_completed = 0

    for phase in phases:
        milestones = phase.get("milestones", [])
        milestone_total += len(milestones)
        milestone_completed += sum(1 for m in milestones if m.get("status") == "completed")

        for milestone in milestones:
            tasks = milestone.get("tasks", [])
            task_total += len(tasks)
            task_completed += sum(1 for t in tasks if t.get("status") == "completed")

    summary["phases"] = {
        "total": phase_total,
        "pending": phase_total - phase_completed,
        "completed": phase_completed
    }
    summary["milestones"] = {
        "total": milestone_total,
        "pending": milestone_total - milestone_completed,
        "completed": milestone_completed
    }
    summary["tasks"] = {
        "total": task_total,
        "pending": task_total - task_completed,
        "completed": task_completed
    }

    roadmap["summary"] = summary


def run_auto_resolver() -> tuple[bool, list[str]]:
    """
    Main function to run the auto-resolver.
    Returns (success, list of resolution messages).
    """
    version = get_current_version()
    if not version:
        return False, ["Could not retrieve current_version from product.json"]

    roadmap_path = get_roadmap_path(version)
    roadmap = load_roadmap(roadmap_path)
    if roadmap is None:
        return False, [f"Could not load roadmap from: {roadmap_path}"]

    resolutions = resolve_milestones_and_phases(roadmap)

    # Update current pointer to next pending task
    current_msg = update_current(roadmap)
    if current_msg:
        resolutions.append(current_msg)

    # Always update summary to ensure counts are accurate
    update_summary(roadmap)
    if not save_roadmap(roadmap_path, roadmap):
        return False, ["Failed to save roadmap after auto-resolution"]

    return True, resolutions


if __name__ == "__main__":
    import sys

    success, messages = run_auto_resolver()

    for msg in messages:
        print(msg, file=sys.stderr)

    sys.exit(0 if success else 1)
