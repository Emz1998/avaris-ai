# Status Validator Hook

PreToolUse hook that validates `project/status.json` structure before Write or Edit operations.

## Purpose

Prevents invalid changes to the project status file by validating against the Pydantic schema defined in `.claude/hooks/project_status/schema.py`.

## How It Works

1. Intercepts `Edit` and `Write` tool calls targeting `project/status.json`
2. For **Write**: Validates the new content directly
3. For **Edit**: Reads current file, applies the edit, validates the result
4. **Blocks** the operation (exit code 2) if validation fails
5. **Allows** the operation (exit code 0) if validation passes

## Schema Reference

Imports and uses `ProjectStatus` model from `project_status/schema.py`, which validates:

- `project`: name, version, target_release, status
- `specs`: prd, tech, ux specification items
- `summary`: phase/milestone/task counts
- `current`: active phase/milestone/task
- `phases`: nested phase -> milestone -> task structure
- `metadata`: last_updated, schema_version

## Configuration

Added to `.claude/settings.local.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "uv run \"$CLAUDE_PROJECT_DIR/.claude/hooks/status_validator/validate_status.py\"",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

## Testing

```bash
# Valid JSON (exit 0)
echo '{"tool_name": "Write", "tool_input": {"file_path": "project/status.json", "content": "{...valid...}"}}' | uv run .claude/hooks/status_validator/validate_status.py

# Invalid JSON (exit 2)
echo '{"tool_name": "Write", "tool_input": {"file_path": "project/status.json", "content": "{}"}}' | uv run .claude/hooks/status_validator/validate_status.py
```
