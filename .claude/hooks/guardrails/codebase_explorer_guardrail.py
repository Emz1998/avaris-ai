#!/usr/bin/env python3
"""
Guardrail hook for codebase-explorer subagent.

This hook operates across multiple events:
- PreToolUse (Task matcher): Detects codebase-explorer subagent start, activates guardrail
- PreToolUse (Write|Edit): Validates file path during active guardrail
- SubagentStop: Detects subagent completion, deactivates guardrail

Blocks during active guardrail:
- Write/Edit to files outside allowed path pattern:
  project/{version}/phases/milestones/{milestone}/codebase-status/codebase-status_{date}_{session_id}.md
"""
import re
import sys
from datetime import datetime
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

# Target subagent this guardrail applies to
TARGET_SUBAGENT = "codebase-explorer"

# Cache key for guardrail state
GUARDRAIL_CACHE_KEY = "codebase_explorer_guardrail_active"

# Tools that are guarded (only allowed on specific paths)
GUARDED_TOOLS = {"Write", "Edit"}


def is_guardrail_active() -> bool:
    """Check if codebase-explorer guardrail is currently active."""
    return get_cache(GUARDRAIL_CACHE_KEY) is True


def activate_guardrail() -> None:
    """Activate the codebase-explorer guardrail in cache."""
    cache = load_cache()
    cache[GUARDRAIL_CACHE_KEY] = True
    write_cache(cache)


def deactivate_guardrail() -> None:
    """Deactivate the codebase-explorer guardrail in cache."""
    cache = load_cache()
    cache[GUARDRAIL_CACHE_KEY] = False
    write_cache(cache)


def get_milestone_folder_name(roadmap: dict, milestone_id: str) -> str | None:
    """Get milestone folder name in format MS-NNN_description."""
    _, milestone = find_milestone_in_roadmap(roadmap, milestone_id)
    if not milestone:
        return None

    ms_id = milestone.get("id", "")
    ms_name = milestone.get("name", "")

    if not ms_id:
        return None

    # Format: MS-NNN_description (slugified)
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", ms_name.lower()).strip("-")
    return f"{ms_id}_{slug}"


def build_allowed_path_pattern(
    version: str, milestone_folder: str, session_id: str
) -> str:
    """Build regex pattern for allowed file paths."""
    date_pattern = r"\d{4}-\d{2}-\d{2}"
    # Escape special regex chars in version and milestone
    version_escaped = re.escape(version)
    milestone_escaped = re.escape(milestone_folder)
    session_escaped = re.escape(session_id)

    pattern = (
        rf"project/{version_escaped}/phases/milestones/"
        rf"{milestone_escaped}/codebase-status/"
        rf"codebase-status_{date_pattern}_{session_escaped}\.md$"
    )
    return pattern


def is_allowed_path(file_path: str) -> tuple[bool, str]:
    """Check if file path matches the allowed pattern."""
    # Get version
    version = get_current_version()
    if not version:
        return False, "Could not determine current version"

    # Get roadmap and current milestone
    roadmap_path = get_roadmap_path(version)
    roadmap = load_roadmap(roadmap_path)
    if not roadmap:
        return False, f"Could not load roadmap from {roadmap_path}"

    current = roadmap.get("current", {})
    milestone_id = current.get("milestone")
    if not milestone_id:
        return False, "No current milestone set in roadmap"

    # Get milestone folder name
    milestone_folder = get_milestone_folder_name(roadmap, milestone_id)
    if not milestone_folder:
        return False, f"Could not find milestone {milestone_id}"

    # Get session ID
    session_id = get_cache("session_id") or ""
    if not session_id:
        return False, "No session_id in cache"

    # Build and check pattern
    pattern = build_allowed_path_pattern(version, milestone_folder, session_id)

    if re.search(pattern, file_path):
        return True, ""

    # Build example path for error message
    today = datetime.now().strftime("%Y-%m-%d")
    expected = (
        f"project/{version}/phases/milestones/{milestone_folder}/"
        f"codebase-status/codebase-status_{today}_{session_id}.md"
    )
    return False, f"Expected path like: {expected}"


def handle_task_pretool(input_data: dict) -> None:
    """
    Handle PreToolUse for Task tool.
    Detects codebase-explorer subagent start and activates guardrail.
    """
    tool_input = input_data.get("tool_input", {})
    subagent_type = tool_input.get("subagent_type", "")

    if subagent_type == TARGET_SUBAGENT:
        activate_guardrail()


def handle_tool_pretool(input_data: dict) -> None:
    """
    Handle PreToolUse for Write|Edit tools.
    Validates file path if guardrail is active.
    """
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
            f"GUARDRAIL: {tool_name} blocked for codebase-explorer subagent. "
            f"Only codebase-status files are allowed. {reason}"
        )


def handle_subagent_stop() -> None:
    """
    Handle SubagentStop event.
    Deactivates guardrail when codebase-explorer subagent completes.
    """
    if is_guardrail_active():
        deactivate_guardrail()


def main() -> None:
    """Entry point for the hook."""
    input_data = read_stdin_json()
    if not input_data:
        sys.exit(0)

    hook_event = input_data.get("hook_event_name", "")
    tool_name = input_data.get("tool_name", "")

    # Route to appropriate handler based on event type
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
