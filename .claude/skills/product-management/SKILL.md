---
name: generating-product-prds
description: Generates Product Requirements Documents (PRDs) in JSON format following the product.json schema. Use when creating new products, defining features, writing user stories, or when user mentions PRD, product requirements, or product definition.
---

**Goal**: Generate structured PRD JSON files that define products, versions, features, user stories, and requirements.

**IMPORTANT**: All generated JSON must conform to the schema in [references/schema.md](references/schema.md).

## Workflow

1. Read app vision: `project/executive/app-vision.md` (primary context source)
2. Read schema: [references/schema.md](references/schema.md)
3. Reference sample structure: [references/sample_product.json](references/sample_product.json)
4. Extract product information from app vision, ask user for any missing details
5. Generate `product.json` at `project/product.json`
6. Validate JSON structure against schema

**Note**: The app-vision.md provides strategic context (vision, problem, solutions, goals) that informs the PRD structure.

## Information Gathering

Ask user for (in order of priority):

### Required - Overview
- Product name and type
- Elevator pitch (1-2 sentences)
- Industry problem being solved
- Solution approaches
- Measurable goals

### Required - Versioning
- Current development version
- Target stable version
- Version release dates

### Required - Features (per version)
- Feature name and description
- User stories (As a [role], I want [action], so that [benefit])
- Acceptance criteria (Given [context], when [action], then [outcome])
- Functional requirements
- Non-functional requirements
- Dependencies and assumptions
- Risks with impact, probability, and mitigation
- Success criteria

### Required - Technical
- Tech stack

## Output Structure

```json
{
  "current_version": "v0.1.0",
  "stable_version": "v1.0.0",
  "overview": { ... },
  "versions": [ ... ],
  "tech_stack": [ ... ],
  "metadata": { ... }
}
```

## ID Conventions

| Prefix | Entity | Example |
|--------|--------|---------|
| `F` | Feature | `F001` |
| `US` | User Story | `US-001` |
| `AC` | Acceptance Criteria | `AC-001` |
| `FR` | Functional Requirement | `FR-001` |
| `NFR` | Non-Functional Requirement | `NFR-001` |
| `D` | Dependency | `D001` |
| `R` | Risk | `R001` |
| `SC` | Success Criteria | `SC-001` |

## Rules

- Use semantic versioning with `v` prefix (e.g., `v1.0.0`)
- All dates in ISO 8601 format (`YYYY-MM-DD`)
- IDs must be unique within their scope
- User stories must follow: "As a [role], I want [action], so that [benefit]"
- Acceptance criteria must use Gherkin format: "Given [context], when [action], then [outcome]"
- Risk probability values: `Low`, `Medium`, `High`
- Version status values: `not_started`, `in_progress`, `completed`, `released`

## Acceptance Criteria

- JSON saved to `project/product.json`
- All required fields present per schema
- Valid JSON syntax
- IDs follow naming conventions
- Metadata includes current date and author
