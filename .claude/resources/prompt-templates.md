# Claude Code Prompt Templates

A collection of reusable prompt patterns for effective Claude Code interactions.

**Important:** Please choose the appropriate template below based on user prompt

---

## Task Implementation

```
Implement [feature name]

Context:
- Location: [file path or module]
- Related code: [dependencies, existing patterns to follow]

Requirements:
- [Requirement 1]
- [Requirement 2]

Constraints:
- [Tech stack, patterns, conventions]
- [Performance considerations]

Acceptance criteria:
- [What "done" looks like]
```

---

## Bug Fix

```
Fix: [brief description of the bug]

Observed behavior:
[What's happening]

Expected behavior:
[What should happen]

Reproduction steps:
1. [Step 1]
2. [Step 2]

Relevant files:
- [file paths]

Error messages (if any):
[paste errors]
```

---

## Refactor

```
Refactor [target code/module]

Current issues:
- [Problem 1: e.g., duplication, complexity, poor naming]
- [Problem 2]

Goals:
- [Improved readability / performance / maintainability]

Constraints:
- No behavior changes
- Maintain existing tests
- [Other constraints]
```

---

## Code Review

```
Review [file or PR description]

Focus areas:
- [ ] Correctness
- [ ] Error handling
- [ ] Edge cases
- [ ] Performance
- [ ] Security
- [ ] Readability
- [ ] Test coverage

Context:
[What this code does, why it was written]
```

---

## Test Generation

```
Write tests for [module/function]

Test framework: [Vitest / Jest / etc.]

Coverage needed:
- [ ] Happy path
- [ ] Edge cases
- [ ] Error conditions
- [ ] Boundary values

Mocking requirements:
- [External dependencies to mock]

Existing patterns:
- [Reference existing test files for style]
```

---

## Architecture / Design

```
Design [system/feature]

Problem:
[What we're solving]

Requirements:
- Functional: [what it must do]
- Non-functional: [scale, performance, security]

Constraints:
- [Existing tech stack]
- [Integration points]

Questions to address:
- [Data flow?]
- [State management?]
- [Error handling strategy?]
```

---

## Documentation

```
Document [target]

Type: [README / API docs / inline comments / architecture doc]

Audience: [developers / users / future self]

Include:
- [ ] Overview / purpose
- [ ] Setup instructions
- [ ] Usage examples
- [ ] API reference
- [ ] Common issues
```

---

## Exploration / Research

```
Explore: [topic or problem]

Context:
[Why I'm looking into this]

Questions:
1. [Question 1]
2. [Question 2]

Constraints:
- [Tech stack limitations]
- [Time/complexity budget]

Output format:
- [Summary with recommendations / comparison table / proof of concept]
```

---

## Quick Patterns

### One-liner tasks

```
Add error handling to [function] for [edge case]
```

```
Extract [logic] from [file] into a reusable util
```

```
Add types to [file/function]
```

```
Rename [x] to [y] across the codebase
```

### Conversational prompts

```
Walk me through how [system/feature] works
```

```
What's the best way to [accomplish X] given [constraints]?
```

```
Compare [approach A] vs [approach B] for [use case]
```

---

## CLAUDE.md Template

```markdown
# Project: [Name]

## Overview

[One paragraph description]

## Tech Stack

- [Framework]
- [Language + version]
- [Key libraries]

## Project Structure
```

src/
components/ # [description]
utils/ # [description]
...

```

## Conventions
- [Naming conventions]
- [File organization]
- [Import ordering]
- [Error handling patterns]

## Commands
- `npm run dev` - [description]
- `npm test` - [description]

## Current Focus
- [Active feature/area]
- [Known issues]

## Gotchas
- [Non-obvious things that cause problems]
```

---

## Tips for Effective Prompts

1. **Be specific about location** - File paths, function names, line numbers
2. **Provide context** - Why, not just what
3. **State constraints upfront** - Tech stack, patterns, performance needs
4. **Define done** - What does success look like?
5. **Include examples** - Reference existing code patterns to follow
6. **One task per prompt** - Avoid bundling unrelated work
