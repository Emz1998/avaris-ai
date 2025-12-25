#!/usr/bin/env python3
"""
Guardrail hook for planning-specialist subagent.

Only allows Write/Edit to: project/{version}/phases/milestones/{milestone}/plans/
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import (
    read_stdin_json,
    get_cache,
    load_cache,
    write_cache,
    block_response,
)
from utils.roadmap import (
    get_current_version,
    get_roadmap_path,
    load_roadmap,
    find_milestone_in_roadmap,
)

TARGET_SUBAGENT = "planning-specialist"
GUARDRAIL_CACHE_KEY = "planner_guardrail_active"
GUARDED_TOOLS = {"Write", "Edit"}


def is_guardrail_active() -> bool:
    return get_cache(GUARDRAIL_CACHE_KEY) is True


def activate_guardrail() -> None:
    cache = load_cache()
    cache[GUARDRAIL_CACHE_KEY] = True
    write_cache(cache)


def deactivate_guardrail() -> None:
    cache = load_cache()
    cache[GUARDRAIL_CACHE_KEY] = False
    write_cache(cache)


def get_milestone_folder_name(roadmap: dict, milestone_id: str) -> str | None:
    _, milestone = find_milestone_in_roadmap(roadmap, milestone_id)
    if not milestone:
        return None
    ms_id = milestone.get("id", "")
    ms_name = milestone.get("name", "")
    if not ms_id:
        return None
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", ms_name.lower()).strip("-")
    return f"{ms_id}_{slug}"


def build_allowed_path_pattern(
    version: str, milestone_folder: str, session_id: str
) -> str:
    """Build regex pattern for allowed file path."""
    date_pattern = r"\d{4}-\d{2}-\d{2}"
    version_escaped = re.escape(version)
    milestone_escaped = re.escape(milestone_folder)
    session_escaped = re.escape(session_id)

    pattern = (
        rf"project/{version_escaped}/phases/milestones/"
        rf"{milestone_escaped}/plans/"
        rf"plan_{date_pattern}_{session_escaped}\.md$"
    )
    return pattern


def is_allowed_path(file_path: str) -> tuple[bool, str]:
    version = get_current_version()
    if not version:
        return False, "Could not determine current version"

    roadmap_path = get_roadmap_path(version)
    roadmap = load_roadmap(roadmap_path)
    if not roadmap:
        return False, f"Could not load roadmap from {roadmap_path}"

    current = roadmap.get("current", {})
    milestone_id = current.get("milestone")
    if not milestone_id:
        return False, "No current milestone set in roadmap"

    milestone_folder = get_milestone_folder_name(roadmap, milestone_id)
    if not milestone_folder:
        return False, f"Could not find milestone {milestone_id}"

    session_id = get_cache("session_id") or ""
    if not session_id:
        return False, "No session_id in cache"

    pattern = build_allowed_path_pattern(version, milestone_folder, session_id)

    if re.search(pattern, file_path):
        return True, ""

    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")
    expected = (
        f"project/{version}/phases/milestones/{milestone_folder}/plans/"
        f"plan_{today}_{session_id}.md"
    )
    return False, f"Expected: {expected}"


def handle_task_pretool(input_data: dict) -> None:
    tool_input = input_data.get("tool_input", {})
    subagent_type = tool_input.get("subagent_type", "")
    if subagent_type == TARGET_SUBAGENT:
        activate_guardrail()


def handle_tool_pretool(input_data: dict) -> None:
    if not is_guardrail_active():
        return

    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    if tool_name not in GUARDED_TOOLS:
        return

    file_path = tool_input.get("file_path", "")
    allowed, reason = is_allowed_path(file_path)

    if not allowed:
        block_response(
            f"GUARDRAIL: {tool_name} blocked for {TARGET_SUBAGENT}. {reason}"
        )


def handle_subagent_stop() -> None:
    if is_guardrail_active():
        deactivate_guardrail()


def main() -> None:
    input_data = read_stdin_json()
    if not input_data:
        sys.exit(0)

    hook_event = input_data.get("hook_event_name", "")
    tool_name = input_data.get("tool_name", "")

    if hook_event == "PreToolUse":
        if tool_name == "Task":
            handle_task_pretool(input_data)
        else:
            handle_tool_pretool(input_data)
    elif hook_event == "SubagentStop":
        handle_subagent_stop()

    sys.exit(0)


if __name__ == "__main__":
    main()
