---
name: specs-creator
description: Creates tech specs and UI/UX specs based on feature requirements. Use when user mentions "Create Tech Specs", "Create UI/UX Specs", or needs technical/design documentation for a version.
---

**Goal**: Create or update comprehensive tech specs and UI/UX specs based on feature requirements

## Dependency Chain

```
app-vision.md → PRD.md → tech-specs.md → ui-ux.md
```

## Workflow

1. Read `project/product/PRD.json` to determine current version and features
2. Read `project/executive/app-vision.md` for project vision
3. For tech-specs: also read `project/product/PRD.md` for requirements
4. For ui-ux specs: read all preceding specs in the dependency chain
5. Choose template from `.claude/skills/specs-creator/templates/`
6. Generate spec with version-specific content
7. Save to `project/{version}/specs/` with correct naming
8. Report completion with file path and next steps

## Constraints

- NEVER create a spec if its dependency doesn't exist yet
- NEVER overwrite existing specs without user approval
- DO NOT create specs outside `project/{version}/specs/` directory
- NEVER assume requirements - ask for clarification
- KEEP specs focused on the target version's features

## Acceptance Criteria

- [ ] Spec contains all required sections from template
- [ ] Frontmatter includes `version-coverage`
- [ ] Database models include future-proofing considerations
- [ ] File saved to `project/{version}/specs/` directory
- [ ] Completion report includes: file path, version, next steps

## References

- **PRD Path:** `project/product/PRD.md`
- **PRD JSON:** `project/product/PRD.json`
- **App Vision:** `project/executive/app-vision.md`
- **Tech Template:** `.claude/skills/specs-creator/templates/tech.md`
- **UX Template:** `.claude/skills/specs-creator/templates/ux.md`

## Considerations

### Per-Version Approach

Tech specs are created per version (e.g., `v0.1.0`, `v0.2.0`). Each version's spec focuses only on features in that release.

**Benefits:**

- Clear scope boundaries per release
- Smaller, focused documents
- Specs can evolve as you learn from previous versions
- Aligns with iterative/MVP development

**Cross-Version Concerns:**

- Use the PRD as the north star for upcoming features
- Design database schemas with nullable fields for future features
- Reference earlier version specs when building on existing systems

### Database Schema Future-Proofing

When designing data models, anticipate future versions:

- Add `type` or `category` columns for entities that may have variants later
- Use nullable fields for attributes coming in future versions
- Prefer additive schema changes (new tables/columns) over modifications
- Document "Future Considerations" for each entity

**Example:**

```
predictions table (v0.1.0):
- prediction_type: 'moneyline' (default)  // Ready for 'spread', 'total' in v1.0.0
- spread_value: null                       // Populated in v1.0.0
- total_value: null                        // Populated in v1.0.0
```

### Frontmatter

Tech specs should include version in YAML frontmatter:

```yaml
---
version: v0.1.0
---
```
