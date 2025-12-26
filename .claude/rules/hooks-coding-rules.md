---
paths: .claude/hooks/**/*.py
---

# Claude Hooks Coding Rules & Patterns

## 1. Module Organization

**Guardrails Pattern**

- Use `GuardrailConfig` and `GuardrailRunner` from `utils.guardrail_base`
- One guardrail per subagent in `guardrails/` directory
- Naming: `{subagent_name}_guardrail.py`

**Utils Pattern**

- Shared utilities in `utils/` directory
- Each utility module has single responsibility
- Export all public functions via `utils/__init__.py`

**Directory Structure**

- `guardrails/` - PreToolUse hooks for subagent control
- `utils/` - Shared helper functions
- `workflow/` - Workflow orchestration hooks
- `status_logger/` - Status tracking hooks
- `security/` - Security validation hooks
- `agent_prompt/` - Prompt modification hooks
- `init_project/` - Project initialization hooks

## 2. Import Patterns

**Standard Import Block**

```python
#!/usr/bin/env python3
"""Module docstring explaining purpose."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import (  # type: ignore
    read_stdin_json,
    block_response,
    get_cache,
)
```

**Rules**

- Always add shebang `#!/usr/bin/env python3`
- Include module docstring at top
- Use `sys.path.insert` to add parent directory for utils imports
- Add `# type: ignore` comment for utils imports
- Import only what you need from utils

## 3. Guardrail Implementation

**Configuration Pattern**

```python
config = GuardrailConfig(
    target_subagent="agent-name",
    cache_key="agent_guardrail_active",
    guarded_tools={"Write", "Edit"},
    blocked_tools={"Bash"},
    path_validator=create_session_file_validator("subfolder", "prefix"),
)
```

**Execution Pattern**

```python
if __name__ == "__main__":
    GuardrailRunner(config).run()
```

**Rules**

- Use declarative `GuardrailConfig` instead of imperative logic
- Cache key format: `{agent_name}_guardrail_active`
- Use path validators from `guardrail_base` module
- Keep main block minimal - delegate to `GuardrailRunner`

## 4. Hook Event Handling

**Input Validation**

```python
def main() -> None:
    hook_input = read_stdin_json()
    if not hook_input:
        sys.exit(0)

    hook_event = hook_input.get("hook_event_name", "")
    tool_name = hook_input.get("tool_name", "")
```

**Exit Codes**

- `sys.exit(0)` - Allow operation
- `sys.exit(2)` - Block operation

**Output Methods**

- `block_response(reason)` - Block with error message to stderr
- `success_response(event, context)` - Success with JSON output
- `log(message)` - Write to stderr for debugging

## 5. Cache Operations

**Reading Cache**

```python
from utils import get_cache, load_cache

is_active = get_cache("key_name")
cache = load_cache()
value = cache.get("key_name")
```

**Writing Cache**

```python
from utils import set_cache, load_cache, write_cache

set_cache("key", value)

# Bulk operations
cache = load_cache()
cache["key1"] = value1
cache["key2"] = value2
write_cache(cache)
```

**Rules**

- Use `get_cache()` for single reads
- Use `set_cache()` for single writes
- Use `load_cache()` + `write_cache()` for bulk operations
- Cache keys should be descriptive snake_case

## 6. Path Validation

**Available Validators**

- `create_directory_validator(subfolder)` - Allow milestone subfolder
- `create_session_file_validator(subfolder, prefix)` - Session-specific files
- `create_pattern_validator(patterns, allow_match, msg)` - Regex patterns
- `create_extension_blocker(ext, except_files)` - Block file extensions

**Custom Validators**

```python
def custom_validator(file_path: str) -> tuple[bool, str]:
    if condition_met(file_path):
        return True, ""
    return False, "Reason for blocking"
```

**Rules**

- Return tuple: `(allowed: bool, reason: str)`
- Empty reason string when allowed
- Clear error message when blocked

## 7. Error Handling

**Defensive Checks**

```python
if not input_data:
    sys.exit(0)

if not get_cache("is_active"):
    sys.exit(0)

tool_name = input_data.get("tool_name", "")
if not tool_name:
    sys.exit(0)
```

**Rules**

- Exit early for invalid/missing input
- Use `.get()` with defaults for dict access
- Never assume keys exist in input data

## 8. Function Design

**Single Responsibility**

- Each function does one thing
- Extract complex logic into helpers
- Keep functions under 30 lines

**Type Hints**

```python
def get_milestone_context() -> tuple[str, str, str] | tuple[None, None, str]:
    """Get version, milestone folder, and session_id."""
    # Implementation
```

**Rules**

- Always use type hints for parameters and return values
- Use descriptive names: `get_`, `is_`, `validate_`, `create_`
- Document complex return types in docstring

## 9. Naming Conventions

**Files and Directories**

- Use `kebab-case` for directories and files
- Suffix guardrails with `_guardrail.py`
- Suffix loggers with `_logger.py`
- Suffix guards with `_guard.py`

**Variables and Functions**

- Use `snake_case` for all variables and functions
- Use `UPPER_SNAKE_CASE` for constants
- Prefix booleans: `is_`, `has_`, `can_`, `should_`

**Cache Keys**

- Format: `{component}_{purpose}_active`
- Examples: `code_reviewer_guardrail_active`, `session_id`, `current_phase`

## 10. Common Patterns

**Activation Pattern**

```python
def is_active() -> bool:
    return get_cache("component_active") is True

def activate() -> None:
    cache = load_cache()
    cache["component_active"] = True
    write_cache(cache)
```

**Milestone Context Pattern**

```python
version, milestone_folder, session_id = get_milestone_context()
if version is None:
    block_response(session_id)  # session_id contains error message
```

**Tool Blocking Pattern**

```python
if tool_name in blocked_tools:
    block_response(f"GUARDRAIL: {tool_name} blocked for {subagent}.")
```

## 11. Best Practices

**Do**

- Use existing validators before creating custom ones
- Keep guardrail config declarative
- Exit early for invalid states
- Use type hints consistently
- Write clear error messages
- Follow DRY principle

**Dont**

- Mix multiple responsibilities in one hook
- Hardcode paths or values - use config
- Ignore type hints or use `Any`
- Write multi-line comments (use docstrings)
- Duplicate logic across hooks - extract to utils
- Create complex conditional logic in hooks

## 12. Testing Considerations

**Testable Design**

- Pure functions with clear inputs/outputs
- Minimal global state access
- Dependency injection via parameters
- Separate logic from I/O operations

**Debug Support**

- Use `log()` for debugging output
- Include context in error messages
- Print to stderr for hook system visibility
