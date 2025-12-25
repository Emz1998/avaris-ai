---
name: discuss
description: Interactive discussion session with AI agents for implementation strategy and decision-making
allowed-tools: Bash(python:*)
model: opus
---

**Goal**: Gather multiple opinions to explore implementation strategies and make decisions for the current task

## Workflow

### Phase 1: Context Gathering

- Deploy @agent-consultant to discuss about how to implement the current task in the roadmap.
- Use `Skill` tool to run /discuss:gpt to get second opinion about the implementation strategy.
- Use `Skill` tool to run /discuss:gemini to get third opinion about the implementation strategy.
