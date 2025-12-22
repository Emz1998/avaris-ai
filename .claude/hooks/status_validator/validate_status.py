#!/usr/bin/env python3
"""
PreToolUse hook to validate project/status.json structure.
Blocks Edit/Write operations if the resulting JSON would be invalid.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

# Add parent directory to path to import from project_status
sys.path.insert(0, str(Path(__file__).parent.parent))

from project_status.schema import ProjectStatus
from pydantic import ValidationError


TARGET_FILE = "project/status.json"


def get_project_dir() -> Path:
    """Get the project directory from environment or fallback to cwd."""
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR")
    if project_dir:
        return Path(project_dir)
    return Path.cwd()


def is_target_file(file_path: str) -> bool:
    """Check if the file path targets project/status.json."""
    project_dir = get_project_dir()
    target_path = project_dir / TARGET_FILE
    try:
        file_path_resolved = Path(file_path).resolve()
        target_path_resolved = target_path.resolve()
        return file_path_resolved == target_path_resolved
    except Exception:
        return False


def validate_json_content(content: str) -> tuple[bool, str]:
    """Validate JSON content against ProjectStatus schema."""
    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"
    try:
        ProjectStatus.model_validate(data)
        return True, ""
    except ValidationError as e:
        errors = []
        for error in e.errors():
            loc = " -> ".join(str(l) for l in error["loc"])
            msg = error["msg"]
            errors.append(f"  {loc}: {msg}")
        return False, "Schema validation failed:\n" + "\n".join(errors)


def apply_edit(original: str, old_string: str, new_string: str) -> str:
    """Apply an edit operation to the original content."""
    return original.replace(old_string, new_string, 1)


def handle_write(tool_input: dict) -> tuple[bool, str]:
    """Handle Write tool validation."""
    file_path = tool_input.get("file_path", "")
    if not is_target_file(file_path):
        return True, ""
    content = tool_input.get("content", "")
    return validate_json_content(content)


def handle_edit(tool_input: dict) -> tuple[bool, str]:
    """Handle Edit tool validation."""
    file_path = tool_input.get("file_path", "")
    if not is_target_file(file_path):
        return True, ""
    old_string = tool_input.get("old_string", "")
    new_string = tool_input.get("new_string", "")
    project_dir = get_project_dir()
    target_path = project_dir / TARGET_FILE
    try:
        original_content = target_path.read_text()
    except FileNotFoundError:
        return False, f"Target file not found: {target_path}"
    except Exception as e:
        return False, f"Error reading file: {e}"
    if old_string not in original_content:
        return True, ""
    new_content = apply_edit(original_content, old_string, new_string)
    return validate_json_content(new_content)


def main():
    """Main entry point for the hook."""
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Hook error: Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)
    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})
    if tool_name == "Write":
        valid, error = handle_write(tool_input)
    elif tool_name == "Edit":
        valid, error = handle_edit(tool_input)
    else:
        sys.exit(0)
    if not valid:
        print(f"status.json validation failed:\n{error}", file=sys.stderr)
        sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
