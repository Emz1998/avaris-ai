#!/usr/bin/env python3
# Roadmap utilities for status loggers

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
    """Save roadmap.json file with updated timestamp."""
    try:
        roadmap["metadata"]["last_updated"] = datetime.now(timezone.utc).isoformat()
        with open(roadmap_path, "w") as f:
            json.dump(roadmap, f, indent=2)
        return True
    except IOError:
        return False


def find_task_in_roadmap(
    roadmap: dict, task_id: str
) -> tuple[dict | None, dict | None, dict | None]:
    """Find task in roadmap. Returns (phase, milestone, task) or (None, None, None)."""
    phases = roadmap.get("phases", [])
    for phase in phases:
        milestones = phase.get("milestones", [])
        for milestone in milestones:
            tasks = milestone.get("tasks", [])
            for task in tasks:
                if task.get("id") == task_id:
                    return phase, milestone, task
    return None, None, None


def find_ac_in_roadmap(roadmap: dict, ac_id: str) -> tuple[dict | None, dict | None]:
    """Find acceptance criteria in roadmap. Returns (task, ac_entry) or (None, None)."""
    phases = roadmap.get("phases", [])
    for phase in phases:
        milestones = phase.get("milestones", [])
        for milestone in milestones:
            tasks = milestone.get("tasks", [])
            for task in tasks:
                acceptance_criteria = task.get("acceptance_criteria", [])
                for ac in acceptance_criteria:
                    id_reference = ac.get("id_reference", "")
                    if ac_id == id_reference:
                        return task, ac
    return None, None


def find_sc_in_roadmap(roadmap: dict, sc_id: str) -> tuple[dict | None, dict | None]:
    """Find success criteria in roadmap. Returns (milestone, sc_entry) or (None, None)."""
    phases = roadmap.get("phases", [])
    for phase in phases:
        milestones = phase.get("milestones", [])
        for milestone in milestones:
            success_criteria = milestone.get("success_criteria", [])
            for sc in success_criteria:
                id_reference = sc.get("id_reference", "")
                if sc_id == id_reference:
                    return milestone, sc
    return None, None


def get_unmet_acs(task: dict) -> list[str]:
    """Get list of unmet acceptance criteria IDs for a task."""
    unmet = []
    for ac in task.get("acceptance_criteria", []):
        if ac.get("status") != "met":
            unmet.append(ac.get("id_reference", "unknown"))
    return unmet


def get_unmet_scs(milestone: dict) -> list[str]:
    """Get list of unmet success criteria IDs for a milestone."""
    unmet = []
    for sc in milestone.get("success_criteria", []):
        if sc.get("status") != "met":
            unmet.append(sc.get("id_reference", "unknown"))
    return unmet


def all_acs_met(task: dict) -> bool:
    """Check if all acceptance criteria for a task are met."""
    acs = task.get("acceptance_criteria", [])
    if not acs:
        return True
    return all(ac.get("status") == "met" for ac in acs)


def all_scs_met(milestone: dict) -> bool:
    """Check if all success criteria for a milestone are met."""
    scs = milestone.get("success_criteria", [])
    if not scs:
        return True
    return all(sc.get("status") == "met" for sc in scs)


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
    """Auto-resolve milestones and phases based on their children's status."""
    resolutions = []
    phases = roadmap.get("phases", [])

    for phase in phases:
        milestones = phase.get("milestones", [])

        for milestone in milestones:
            current_status = milestone.get("status")
            tasks_completed = all_tasks_completed(milestone)
            scs_met = all_scs_met(milestone)

            if current_status != "completed" and tasks_completed:
                if not scs_met:
                    unmet = get_unmet_scs(milestone)
                    resolutions.append(
                        f"Milestone '{milestone.get('id')}' cannot be completed. "
                        f"Unmet success criteria: {', '.join(unmet)}"
                    )
                else:
                    milestone["status"] = "completed"
                    resolutions.append(
                        f"Milestone '{milestone.get('id')}' auto-resolved to 'completed'"
                    )
            elif current_status == "completed" and not tasks_completed:
                milestone["status"] = "in_progress"
                resolutions.append(
                    f"Milestone '{milestone.get('id')}' reverted to 'in_progress'"
                )

        current_phase_status = phase.get("status")
        milestones_completed = all_milestones_completed(phase)

        if current_phase_status != "completed" and milestones_completed:
            phase["status"] = "completed"
            resolutions.append(
                f"Phase '{phase.get('id')}' auto-resolved to 'completed'"
            )
        elif current_phase_status == "completed" and not milestones_completed:
            phase["status"] = "in_progress"
            resolutions.append(f"Phase '{phase.get('id')}' reverted to 'in_progress'")

    return resolutions


def update_current_pointer(roadmap: dict) -> str | None:
    """Update the 'current' section to point to the next pending task."""
    phases = roadmap.get("phases", [])
    current = roadmap.get("current", {})
    old_current = (current.get("phase"), current.get("milestone"), current.get("task"))

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
            "task": new_task_id,
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
        milestone_completed += sum(
            1 for m in milestones if m.get("status") == "completed"
        )

        for milestone in milestones:
            tasks = milestone.get("tasks", [])
            task_total += len(tasks)
            task_completed += sum(1 for t in tasks if t.get("status") == "completed")

    summary["phases"] = {
        "total": phase_total,
        "pending": phase_total - phase_completed,
        "completed": phase_completed,
    }
    summary["milestones"] = {
        "total": milestone_total,
        "pending": milestone_total - milestone_completed,
        "completed": milestone_completed,
    }
    summary["tasks"] = {
        "total": task_total,
        "pending": task_total - task_completed,
        "completed": task_completed,
    }

    roadmap["summary"] = summary


def run_auto_resolver() -> tuple[bool, list[str]]:
    """Run the auto-resolver for milestones and phases."""
    version = get_current_version()
    if not version:
        return False, ["Could not retrieve current_version from product.json"]

    roadmap_path = get_roadmap_path(version)
    roadmap = load_roadmap(roadmap_path)
    if roadmap is None:
        return False, [f"Could not load roadmap from: {roadmap_path}"]

    resolutions = resolve_milestones_and_phases(roadmap)

    current_msg = update_current_pointer(roadmap)
    if current_msg:
        resolutions.append(current_msg)

    update_summary(roadmap)
    if not save_roadmap(roadmap_path, roadmap):
        return False, ["Failed to save roadmap after auto-resolution"]

    return True, resolutions
