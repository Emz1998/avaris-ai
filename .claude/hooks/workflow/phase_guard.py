#!/usr/bin/env python3
"""Guard tool usage based on current workflow phase."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import get_cache, block_response, read_stdin_json  # type: ignore


def get_valid_file_names(session_id: str) -> dict[str, str]:
    """Get valid file name patterns for each phase."""
    return {
        "planning": f"plan_{session_id}",
        "research": f"research_{session_id}",
        "explore": f"explore_{session_id}",
    }


def get_default_reasons(current_phase: str) -> dict[str, str]:
    """Get blocking reasons for each action type."""
    return {
        "coding": f"You are not allowed to code in {current_phase} phase.",
        "planning": f"You are not allowed to plan in {current_phase} phase.",
        "research": f"You are not allowed to research in {current_phase} phase.",
        "commit": f"You are not allowed to commit code in {current_phase} phase.",
        "explore": f"You are not allowed to explore in {current_phase} phase.",
    }


def is_code_file(file_path: str) -> bool:
    """Check if file is a code file."""
    code_extensions = (".ts", ".tsx", ".js", ".jsx", ".json", ".css", ".html", ".py")
    return file_path.endswith(code_extensions)


def block_coding(file_path: str, reason: str) -> None:
    """Block coding operations on code files."""
    if is_code_file(file_path):
        block_response(reason)


def block_planning(file_path: str, valid_name: str, reason: str) -> None:
    """Block planning file operations."""
    if valid_name in file_path:
        block_response(reason)


def block_research(file_path: str, valid_name: str, reason: str) -> None:
    """Block research file operations."""
    if valid_name in file_path:
        block_response(reason)


def block_explore(file_path: str, valid_name: str, reason: str) -> None:
    """Block explore file operations."""
    if valid_name in file_path:
        block_response(reason)


def block_commit(command: str, reason: str) -> None:
    """Block git commit commands."""
    if "git commit" in command:
        block_response(reason)


def setup_phase_guard() -> None:
    """Main phase guard logic."""
    try:
        hook_input = read_stdin_json()
        tool_name = hook_input.get("tool_name", "")

        # Only guard Write and Bash tools
        if tool_name not in ("Write", "Bash"):
            sys.exit(0)

        # Get current phase and session from cache
        current_phase = get_cache("current_phase")
        session_id = get_cache("session_id") or ""

        if not current_phase:
            sys.exit(0)

        # Get file path and command from tool input
        tool_input = hook_input.get("tool_input", {})
        file_path = (
            tool_input.get("file_path", "") if isinstance(tool_input, dict) else ""
        )
        command = tool_input.get("command", "") if isinstance(tool_input, dict) else ""

        # Get valid file names and reasons
        valid_names = get_valid_file_names(session_id)
        reasons = get_default_reasons(current_phase)

        # Apply phase-based blocking
        if current_phase == "explore":
            block_research(file_path, valid_names["research"], reasons["research"])
            block_planning(file_path, valid_names["planning"], reasons["planning"])
            block_coding(file_path, reasons["coding"])
        elif current_phase == "research":
            block_planning(file_path, valid_names["planning"], reasons["planning"])
            block_coding(file_path, reasons["coding"])
        elif current_phase == "plan":
            block_coding(file_path, reasons["coding"])
            block_commit(command, reasons["commit"])
        elif current_phase == "code":
            block_commit(command, reasons["commit"])

        sys.exit(0)

    except Exception as e:
        block_response(f"Phase guard error: {e}")


if __name__ == "__main__":
    setup_phase_guard()
