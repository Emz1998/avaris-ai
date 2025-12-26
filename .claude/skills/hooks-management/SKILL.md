---
name: hooks-management
description: Use PROACTIVELY when you need to create, update, configure, or validate Claude hooks for various events and integrations
---

**Goal**: Create, update or troubleshoot Claude Code hook scripts

## Workflow

1. Identify which hook category is relevant to the task
2. Read ONLY the README.md for that specific category (see below)
3. Read references as needed:
   - `references/code-patterns.md` - Common Python patterns
   - `references/input-patterns.md` - JSON input/output schemas
   - `references/hooks.md` - Full hook documentation
4. Create or update the hook script
5. Verify hook execution using `echo` to pipe JSON input
6. Provide report to main agent

## Hook Categories

_Read the category README.md ONLY when working on that category_

| Category         | Purpose                             | README                                  |
| ---------------- | ----------------------------------- | --------------------------------------- |
| `security/`      | Block dangerous commands/paths      | `.claude/hooks/security/README.md`      |
| `guardrails/`    | Subagent permission control         | `.claude/hooks/guardrails/README.md`    |
| `workflow/`      | Phase management, context injection | `.claude/hooks/workflow/README.md`      |
| `status_logger/` | Task/AC/SC logging                  | `.claude/hooks/status_logger/README.md` |
| `init_project/`  | Project initialization              | `.claude/hooks/init_project/README.md`  |
| `agent_prompt/`  | Prompt manipulation                 | `.claude/hooks/agent_prompt/README.md`  |
| `utils/`         | Shared utilities                    | `.claude/hooks/utils/README.md`         |

## Rules

- **NEVER** hardcode credentials or modify critical system files
- **NEVER** write hooks that can cause infinite loops
- **NEVER** bypass security validations
- **DO NOT** use multiline comments. Only single line comments.
- **MUST** include proper error handling
- **MUST** prefer Python over shell scripts
- **MUST** use `sys.path.insert(0, str(Path(__file__).parent.parent))` to import utils
- **MUST** use type hints and type checking
- **MUST** use `# type: ignore` to suppress type errors

## Acceptance Criteria

- Hook executes successfully on target event
- Hook handles invalid/malformed input gracefully
- No security vulnerabilities
- Uses shared utilities from `.claude/hooks/utils/`
