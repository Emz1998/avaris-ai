---
name: specs-creator
description: Use PROACTIVELY this skill when you need to create tech specs and UI/UX specs based on feature description. If the user specify "Create Tech Specs" or "Create UI/UX Specs", this skill must be triggered.
---

**Goal**: Create or update comprehensive tech specs and UI/UX specs based on feature requirements

## Dependency Chain

```
app-vision.md → PRD.md → tech-specs.md → ui-ux.md
```

## Workflow

1. Read and analyze the app-vision.md file to understand the project vision and goals
2. Choose the right template in `.claude/skills/specs-creator/templates/` based on the dependency chain
3. Generate the spec based on the template and the app-vision.md file
4. Provide comprehensive report to user with specs details, location, and usage guidance

**Important**: If the spec type is `tech-specs`, you have to both read the `app-vision.md` and `prd.md` files to understand the architecture and the dependencies
**Important**: If the spec type is `ui-ux`, you have to read all preceding specs to understand the overall product and its system

## Constraints

- NEVER create a spec if its dependency doesn't exist yet (see Dependency Chain)
- NEVER write or modify actual code implementation
- NEVER overwrite existing specs without explicit user approval
- DO NOT make architectural decisions beyond documentation scope
- NEVER skip template compliance validation
- DO NOT create specs outside designated `project/{version}/specs/` directory
- NEVER assume requirements without user clarification

## Acceptance Criteria

- [ ] Generated spec contains all required sections from the corresponding template
- [ ] All placeholder fields in the template are populated with feature-specific content
- [ ] Spec file is saved to `project/{version}/specs/` directory with correct naming convention
- [ ] Completion report includes: file path, spec type, and next steps for the user

## References

- **PRD Path** `project/PRD.md`
- **App Vision Path** `project/executive/app-vision.md`
- To get the version, read `project/product.json`

### Templates

- **Tech Specs Template** `.claude/skills/specs-creator/templates/tech.md`
- **UX Specs Template** `.claude/skills/specs-creator/templates/ux.md`
