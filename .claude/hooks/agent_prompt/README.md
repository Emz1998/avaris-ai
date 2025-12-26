# Agent Prompt Hooks

Hooks for manipulating and refining agent prompts.

## Files

**prompt_refiner.py** - Refines subagent prompts
- Intercepts `Task` tool invocations
- Runs prompt through Claude haiku for refinement
- Returns updated prompt via `hookSpecificOutput`

## How It Works

1. Hook intercepts PreToolUse for Task tool
2. Extracts initial prompt and subagent type
3. Sends prompt to Claude haiku with refinement instruction
4. Returns modified tool_input with refined prompt

## Output Format

```python
output = {
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "updatedInput": {
            "tool_input": {
                "prompt": refined_prompt,
            },
        },
    }
}
```

## Configuration

- Model: haiku (fast and cheap)
- Tools allowed: Read only
- Purpose: Add context without rewriting

## Logs

- `initial_prompt.log` - Original prompt
- `refined_prompt.log` - Refined output
