---
name: test
description: Test the command
allowed-tools: Bash(git add:*), Bash(git commit:*)
argument-hint: [message]
model: sonnet
---

!`git add . && git commit -m "$ARGUMENTS"`

Do not execute the command yourself, just tell me the output.
