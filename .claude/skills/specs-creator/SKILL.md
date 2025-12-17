---
name: specs-creator
description: Use PROACTIVELY this skill when you need to create or update comprehensive PRDs, tech specs, and UI/UX specs based on feature description. If the user specify "Create PRD", "Create Tech Specs", or "Create UI/UX Specs", this skill must be triggered.
---

**Goal**: Create or update comprehensive PRDs, tech specs, and UI/UX specs based on feature requirements

## Dependency Chain

```
brainstorm-summary.md → prd.md → tech-specs.md → ui-ux.md
```

## Workflow

1. Read and analyze the brainstorm-summary.md file to understand the project vision and goals
2. Choose the right template in `.claude/skills/specs-creator/templates/` based on the dependency chain
3. Generate the spec based on the template and the brainstorm-summary.md file
4. Provide comprehensive report to user with specs details, location, and usage guidance

**Important**: If the spec type is `tech-specs`, you have to both read the `brainstorm-summary.md` and `prd.md` files to understand the architecture and the dependencies
**Important**: If the spec type is `ux`, you have to read all preceding specs to understand the design principles and the color system

## Constraints

- NEVER create a spec if its dependency doesn't exist yet (see Dependency Chain)
- NEVER write or modify actual code implementation
- NEVER overwrite existing specs without explicit user approval
- DO NOT make architectural decisions beyond documentation scope
- NEVER skip template compliance validation
- DO NOT create specs outside designated `project/specs/` directory
- NEVER assume requirements without user clarification

## Acceptance Criteria

- [ ] Generated spec contains all required sections from the corresponding template
- [ ] All placeholder fields in the template are populated with feature-specific content
- [ ] Spec file is saved to `specs/` directory with correct naming convention
- [ ] Completion report includes: file path, spec type, and next steps for the user

## Template Paths

- **PRD** `.claude/skills/specs-creator/templates/prd.md`
- **Tech Specs** `.claude/skills/specs-creator/templates/tech-specs.md`
- **UX Specs** `.claude/skills/specs-creator/templates/ux.md`
