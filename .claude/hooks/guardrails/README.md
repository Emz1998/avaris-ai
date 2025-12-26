# Guardrails Hooks

PreToolUse hooks that control subagent permissions and tool access.

## Architecture

Each guardrail uses `GuardrailConfig` and `GuardrailRunner` from utils:

```python
from utils import GuardrailConfig, GuardrailRunner, create_session_file_validator

config = GuardrailConfig(
    target_subagent="agent-name",
    cache_key="agent_guardrail_active",
    guarded_tools={"Write", "Edit"},
    path_validator=create_session_file_validator("subfolder", "prefix"),
)

if __name__ == "__main__":
    GuardrailRunner(config).run()
```

## Available Guardrails

- `code_reviewer_guardrail.py` - Limits code-reviewer to revision files
- `codebase_explorer_guardrail.py` - Limits explorer to explore files
- `engineer_task_logger_guardrail.py` - Blocks implementation tools until task logged as in_progress
- `fullstack_developer_guardrail.py` - Controls developer tool access
- `gemini_manager_guardrail.py` - External AI manager controls
- `gpt_manager_guardrail.py` - External AI manager controls
- `plan_consultant_guardrail.py` - Limits to plan files
- `planner_guardrail.py` - Strategic planner controls
- `project_manager_guardrail.py` - Project manager controls
- `test_engineer_guardrail.py` - Test engineer controls
- `version_manager_guardrail.py` - Version control limits

## GuardrailConfig Options

- `target_subagent` - Subagent type to guard
- `cache_key` - Cache key for activation state
- `guarded_tools` - Tools requiring path validation
- `blocked_tools` - Completely blocked tools
- `allowed_skills` - Whitelist of allowed skills
- `blocked_skills_except` - Block all skills except listed
- `path_validator` - Function to validate file paths
- `block_unsafe_bash` - Block non-safe git commands

## Path Validators

- `create_directory_validator(subfolder)` - Allow writes to milestone subfolder
- `create_session_file_validator(subfolder, prefix)` - Session-specific files
- `create_pattern_validator(patterns, allow_match, error_msg)` - Regex-based
- `create_extension_blocker(ext, except_files)` - Block by extension
