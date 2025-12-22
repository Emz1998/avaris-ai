#!/usr/bin/env python3
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "hooks"))
from utils.json_handler import load_json

MILESTONE_ID_PATTERN = re.compile(r"^MS-\d{3}$")

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
STATUS_FILE = PROJECT_ROOT / "project" / "status.json"
AGENTS_DIR = PROJECT_ROOT / ".claude" / "agents" / "engineers"


def load_status() -> dict[str, Any]:
    return load_json(str(STATUS_FILE))


def save_status(data: dict[str, Any]) -> None:
    data["metadata"]["last_updated"] = datetime.now(timezone.utc).isoformat()
    STATUS_FILE.write_text(json.dumps(data, indent=2))


def update_summary(data: dict[str, Any]) -> None:
    phases = data.get("phases", {})
    phase_count = len(phases)
    phase_completed = sum(1 for p in phases.values() if p.get("status") == "completed")

    milestone_count = 0
    milestone_completed = 0
    task_count = 0
    task_completed = 0

    for phase in phases.values():
        milestones = phase.get("milestones", {})
        milestone_count += len(milestones)
        milestone_completed += sum(1 for m in milestones.values() if m.get("status") == "completed")

        for milestone in milestones.values():
            tasks = milestone.get("tasks", {})
            task_count += len(tasks)
            task_completed += sum(1 for t in tasks.values() if t.get("status") == "completed")

    data["summary"] = {
        "phases": {"total": phase_count, "completed": phase_completed},
        "milestones": {"total": milestone_count, "completed": milestone_completed},
        "tasks": {"total": task_count, "completed": task_completed},
    }


def get_available_subagents() -> list[str]:
    if not AGENTS_DIR.exists():
        return []
    return [f.stem for f in AGENTS_DIR.glob("*.md")]


def validate_subagents(subagents: list[str]) -> tuple[bool, str]:
    available = get_available_subagents()
    invalid = [s for s in subagents if s not in available]
    if invalid:
        return False, f"Invalid subagents: {invalid}. Available: {available}"
    return True, ""


def get_all_milestone_ids(data: dict[str, Any]) -> set[str]:
    milestone_ids: set[str] = set()
    for phase in data.get("phases", {}).values():
        milestone_ids.update(phase.get("milestones", {}).keys())
    return milestone_ids


def validate_milestone_refs(
    refs: list[str], data: dict[str, Any], field_name: str
) -> tuple[bool, str]:
    if not refs:
        return True, ""

    invalid_format = [r for r in refs if not MILESTONE_ID_PATTERN.match(r)]
    if invalid_format:
        return False, f"Invalid {field_name} format: {invalid_format}. Expected: MS-NNN"

    existing_ids = get_all_milestone_ids(data)
    non_existent = [r for r in refs if r not in existing_ids]
    if non_existent:
        return False, f"Non-existent milestones in {field_name}: {non_existent}"

    return True, ""


def add_phase(phase_id: str, name: str) -> dict[str, Any]:
    data = load_status()

    if phase_id in data.get("phases", {}):
        raise ValueError(f"Phase '{phase_id}' already exists")

    phase = {
        "id": f"phase-{phase_id}",
        "name": name,
        "status": "not_started",
        "milestones": {},
    }

    if "phases" not in data:
        data["phases"] = {}
    data["phases"][phase_id] = phase

    update_summary(data)
    save_status(data)

    return phase


def add_milestone(
    phase_id: str,
    milestone_id: str,
    name: str,
    goal: str,
    parallel: bool = False,
    parallel_with: list[str] | None = None,
    dependencies: list[str] | None = None,
) -> dict[str, Any]:
    data = load_status()

    if phase_id not in data.get("phases", {}):
        raise ValueError(f"Phase '{phase_id}' does not exist")

    phase = data["phases"][phase_id]
    if milestone_id in phase.get("milestones", {}):
        raise ValueError(f"Milestone '{milestone_id}' already exists in phase '{phase_id}'")

    parallel_with_list = parallel_with or []
    dependencies_list = dependencies or []

    valid, error = validate_milestone_refs(parallel_with_list, data, "parallel_with")
    if not valid:
        raise ValueError(error)

    valid, error = validate_milestone_refs(dependencies_list, data, "dependencies")
    if not valid:
        raise ValueError(error)

    milestone = {
        "name": name,
        "goal": goal,
        "parallel": parallel,
        "parallel_with": parallel_with_list,
        "dependencies": dependencies_list,
        "status": "not_started",
        "tasks": {},
        "acceptance_criteria": [],
    }

    if "milestones" not in phase:
        phase["milestones"] = {}
    phase["milestones"][milestone_id] = milestone

    update_summary(data)
    save_status(data)

    return milestone


def add_task(
    phase_id: str,
    milestone_id: str,
    task_id: str,
    description: str,
    priority: bool = False,
    subagent_delegation: bool = False,
    subagents: list[str] | None = None,
    dependencies: list[str] | None = None,
) -> dict[str, Any]:
    data = load_status()

    if phase_id not in data.get("phases", {}):
        raise ValueError(f"Phase '{phase_id}' does not exist")

    phase = data["phases"][phase_id]
    if milestone_id not in phase.get("milestones", {}):
        raise ValueError(f"Milestone '{milestone_id}' does not exist in phase '{phase_id}'")

    milestone = phase["milestones"][milestone_id]
    if task_id in milestone.get("tasks", {}):
        raise ValueError(f"Task '{task_id}' already exists in milestone '{milestone_id}'")

    subagents_list = subagents or []
    if subagent_delegation and subagents_list:
        valid, error = validate_subagents(subagents_list)
        if not valid:
            raise ValueError(error)

    task = {
        "description": description,
        "priority": priority,
        "subagent_delegation": subagent_delegation,
        "subagents": subagents_list,
        "dependencies": dependencies or [],
        "status": "not_started",
    }

    if "tasks" not in milestone:
        milestone["tasks"] = {}
    milestone["tasks"][task_id] = task

    update_summary(data)
    save_status(data)

    return task


def add_acceptance_criteria(
    phase_id: str,
    milestone_id: str,
    ac_id: str,
    description: str,
) -> dict[str, Any]:
    data = load_status()

    if phase_id not in data.get("phases", {}):
        raise ValueError(f"Phase '{phase_id}' does not exist")

    phase = data["phases"][phase_id]
    if milestone_id not in phase.get("milestones", {}):
        raise ValueError(f"Milestone '{milestone_id}' does not exist in phase '{phase_id}'")

    milestone = phase["milestones"][milestone_id]
    existing_ids = [ac["id"] for ac in milestone.get("acceptance_criteria", [])]
    if ac_id in existing_ids:
        raise ValueError(f"Acceptance criteria '{ac_id}' already exists in milestone '{milestone_id}'")

    ac = {
        "id": ac_id,
        "description": description,
        "met": False,
    }

    if "acceptance_criteria" not in milestone:
        milestone["acceptance_criteria"] = []
    milestone["acceptance_criteria"].append(ac)

    save_status(data)

    return ac
