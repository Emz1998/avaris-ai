#!/usr/bin/env python3
# Task Status Logger Hook
# PreToolUse hook for Skill matcher to update task status in roadmap.json

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

VALID_STATUSES = ["completed", "in_progress", "blocked"]
TASK_ID_PATTERN = r"^T\d{3}$"


def read_stdin_json() -> dict:
    """Parse JSON from stdin."""
    try:
        return json.load(sys.stdin)
    except json.JSONDecodeError:
        return {}


def log(msg: str) -> None:
    """Print to stderr for visibility."""
    print(msg, file=sys.stderr, flush=True)


def block_response(reason: str) -> None:
    """Output error and exit 2 (blocking)."""
    print(reason, file=sys.stderr)
    sys.exit(2)


def get_project_dir() -> Path:
    """Get project directory from environment or cwd."""
    import os
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


def find_task_in_roadmap(roadmap: dict, task_id: str) -> tuple[dict | None, dict | None, dict | None]:
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


def update_task_status(roadmap_path: Path, task_id: str, new_status: str) -> bool:
    """Update task status in roadmap.json."""
    roadmap = load_roadmap(roadmap_path)
    if roadmap is None:
        return False

    phase, milestone, task = find_task_in_roadmap(roadmap, task_id)
    if task is None:
        return False

    task["status"] = new_status
    roadmap["metadata"]["last_updated"] = datetime.now(timezone.utc).isoformat()

    try:
        with open(roadmap_path, "w") as f:
            json.dump(roadmap, f, indent=2)
        return True
    except IOError:
        return False


def parse_args(args_str: str) -> tuple[str, str] | None:
    """Parse args string in format '<task-id> <status>'. Returns (task_id, status) or None."""
    if not args_str:
        return None

    parts = args_str.strip().split()
    if len(parts) != 2:
        return None

    return parts[0], parts[1]


def validate_task_id(task_id: str) -> bool:
    """Validate task ID format (TNNN)."""
    return bool(re.match(TASK_ID_PATTERN, task_id))


def validate_status(status: str) -> bool:
    """Validate status is one of the valid statuses."""
    return status in VALID_STATUSES


def main() -> None:
    input_data = read_stdin_json()
    if not input_data:
        sys.exit(0)

    # Check if this is a Skill tool call
    tool_name = input_data.get("tool_name", "")
    if tool_name != "Skill":
        sys.exit(0)

    # Get tool_input
    tool_input = input_data.get("tool_input", {})
    skill_name = tool_input.get("skill", "")
    args = tool_input.get("args", "")

    # Only process log:task skill
    if skill_name != "log:task":
        sys.exit(0)

    # Parse args
    parsed = parse_args(args)
    if parsed is None:
        block_response(f"Invalid args format. Expected: '<task-id> <status>'. Example: 'T001 completed'")

    task_id, status = parsed

    # Validate task ID format
    if not validate_task_id(task_id):
        block_response(f"Invalid task ID format: '{task_id}'. Expected format: TNNN (e.g., T001, T002)")

    # Validate status
    if not validate_status(status):
        block_response(f"Invalid status: '{status}'. Valid statuses: {', '.join(VALID_STATUSES)}")

    # Get current version
    version = get_current_version()
    if not version:
        block_response("Could not retrieve current_version from project/product.json")

    # Get roadmap path
    roadmap_path = get_roadmap_path(version)
    if not roadmap_path.exists():
        block_response(f"Roadmap not found at: {roadmap_path}")

    # Load roadmap and validate task exists
    roadmap = load_roadmap(roadmap_path)
    if roadmap is None:
        block_response(f"Could not load roadmap from: {roadmap_path}")

    phase, milestone, task = find_task_in_roadmap(roadmap, task_id)
    if task is None:
        block_response(f"Task '{task_id}' not found in roadmap")

    # Update task status
    if not update_task_status(roadmap_path, task_id, status):
        block_response(f"Failed to update task status for '{task_id}'")

    log(f"Task '{task_id}' status updated to '{status}'")
    sys.exit(0)


if __name__ == "__main__":
    main()
