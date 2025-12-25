# Workflow Hooks Module

Hook scripts for enforcing workflow phases and subagent ordering in the implement workflow.

## Files

**phase_guard.py**

- Hook Event: `PreToolUse`
- Matcher: `Write|Bash`
- Blocks tool usage based on current workflow phase
- Prevents coding in explore/research phases, commits before code phase

**phase_transition_guard.py**

- Hook Event: `PreToolUse`, `UserPromptSubmit`
- Matcher: `SlashCommand`
- Validates phase transitions (no rollbacks, no skipping)
- Tracks completed phases in cache

**subagent_order_validation.py**

- Hook Event: `PreToolUse`
- Matcher: `Task`
- Enforces sequential subagent invocation order
- Blocks backwards transitions and skipping

**context_injector.py**

- Hook Event: `SessionStart`
- Injects project status context into session
- Reads from `project/status.json`

**stop_guard.py**

- Hook Event: `Stop`
- Blocks stoppage when tasks are in progress or incomplete
- Checks roadmap for task statuses
- Uses `continue: true` to allow stop, `decision: block` to prevent

**reset_cache.py**

- Utility script (not a hook)
- Resets workflow cache to default state
- Run manually: `python3 reset_cache.py`

## Phase Order

1. `log:task` - Task logging
2. `explore` - Codebase exploration
3. `discuss` - Discussion/clarification
4. `plan` - Implementation planning
5. `code` - Code implementation
6. `code-review` - Code review
7. `commit` - Version control

## Subagent Order

1. `codebase-explorer`
2. `research-specialist`
3. `research-consultant`
4. `strategic-planner`
5. `plan-consultant`
6. `test-manager`
7. `code-reviewer`
8. `code-specialist`
9. `version-manager`

## Cache Location

All scripts use the shared cache at `.claude/hooks/cache.json`

## Dependencies

- `utils` module from `.claude/hooks/utils/`
- Python 3.10+
