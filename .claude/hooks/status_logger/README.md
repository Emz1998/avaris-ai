# Status Logger

Hook module for logging roadmap item statuses via skill commands.

## Overview

This module provides PreToolUse hooks that intercept `log:*` skill calls and update the corresponding items in `roadmap.json`.

## Files

- `dispatcher.py` - Routes skill calls to appropriate logger
- `task_logger.py` - Handles `log:task` commands
- `ac_logger.py` - Handles `log:ac` (acceptance criteria) commands
- `sc_logger.py` - Handles `log:sc` (success criteria) commands

## Usage

**Log task status:**
```
/log:task <task-id> <status>
```
- Valid statuses: `completed`, `in_progress`, `blocked`
- Auto-resolves parent milestone/phase when all tasks complete

## Guards

**Dependency Guard (in_progress):**
- Task cannot start if its dependencies are not completed
- Task cannot start if parent milestone has incomplete dependencies
- Blocks with list of incomplete dependencies

**Completion Guard (completed):**
- Task cannot be completed if acceptance criteria are not met
- Blocks with list of unmet ACs

**Log acceptance criteria:**
```
/log:ac <ac-id> <status>
```
- Valid statuses: `met`, `unmet`

**Log success criteria:**
```
/log:sc <sc-id> <status>
```
- Valid statuses: `met`, `unmet`

## Dependencies

- `utils.roadmap` - Roadmap file operations
- `utils.output` - Logging and response utilities
- `utils.validation` - Input validation

## Hook Registration

Register `dispatcher.py` as a PreToolUse hook for the `Skill` tool in `settings.local.json`.
