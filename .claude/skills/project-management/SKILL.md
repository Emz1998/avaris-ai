---
name: managing-roadmaps
description: Creates and manages project roadmap.json files with phases, milestones, and tasks. Use when creating roadmaps, adding phases/milestones/tasks, updating status, or when user mentions roadmap management, release planning, or project phases.
---

**Goal**: Create and maintain structured roadmap.json files in `project/v{version}/release-plan/roadmap.json` that track project phases, milestones, and tasks.

**IMPORTANT**: Phases run SEQUENTIALLY. Milestones within a phase run in PARALLEL. If a milestone must run sequentially, place it in its own single-milestone phase.

## Workflow

### Phase 1: Assessment

1. Read `project/product.json` to get current version
2. Construct target path: `project/{version}/release-plan/roadmap.json`
3. Check if roadmap.json exists (determines create vs update)
4. Read `.claude/skills/project-management/references/sample_data.json` and `.claude/skills/project-management/references/schema.md` for schema reference
5. **Read specs for context** (required for create/add operations):
   - `project/{version}/specs/prd.md` - Product requirements, features, user stories
   - `project/{version}/specs/tech-specs.md` - Architecture, data models, APIs
   - `project/{version}/specs/ux.md` - UI components, user flows

### Phase 2: Operation Execution

**Create roadmap:**

- Analyze specs to derive phases, milestones, and tasks
- Extract features from PRD → milestones with goals
- Extract technical requirements from tech-specs → tasks with owners
- Extract UI components from ux.md → tasks for UI development
- Initialize with project metadata (name, version, target_release)
- Set status to "not_started"
- Initialize summary with zeros
- Set metadata with current timestamp and schema_version "1.0.0"

**Add phase:**

- Generate next PH-ID (scan existing, increment max)
- Create phase with empty milestones array
- Append to phases array

**Add milestone:**

- Find target phase by PH-ID
- Generate next MS-ID
- Create milestone with empty tasks and success_criteria arrays
- Append to phase.milestones

**Add task:**

- Find target milestone by MS-ID
- Validate owner against `.claude/agents/engineers/` folder or "main-agent"
- Generate next T-ID
- Create task with empty acceptance_criteria array
- Append to milestone.tasks

**Update status:**

- Find item by ID (PH-xxx, MS-xxx, or Txxx)
- Update status field
- Valid values: "not_started", "in_progress", "completed"

**Mark criteria met:**

- Find criteria by ID (SC-xxx or AC-xxx)
- Set met to true

### Phase 3: Finalization

1. Recompute summary section:
   - Count totals, pending (status != completed), completed
   - Set recently_completed and current items
2. Update `metadata.last_updated` to current ISO 8601 datetime
3. Write to target roadmap.json file
4. Report changes made

## Rules

- **MUST** read specs (prd.md, tech-specs.md, ux.md) before creating or adding to roadmap
- **ID Generation**: Scan all existing IDs of type, find max numeric value, increment by 1, pad to 3 digits
- **ID Patterns**: PH-NNN (phases), MS-NNN (milestones), TNNN (tasks), SC-NNN (success criteria), AC-NNN (acceptance criteria)
- **Valid owners**: "main-agent" or any filename (without .md) in `.claude/agents/engineers/`
- **Valid status**: "not_started", "in_progress", "completed"
- **Milestone dependencies**: Must reference existing MS-IDs from same or previous phases
- **Task dependencies**: Must reference existing T-IDs within the same milestone
- **NEVER** modify phases array order (order determines sequential execution)
- **MUST** recompute summary after every mutation
- **MUST** update metadata.last_updated after every mutation

## Schema Reference

See [references/sample_data.json](references/sample_data.json) for complete JSON structure.

## Acceptance Criteria

- Roadmap.json follows exact structure from sample_data.json
- All IDs follow correct patterns (PH-NNN, MS-NNN, TNNN, SC-NNN, AC-NNN)
- Summary section accurately reflects current counts
- metadata.last_updated is current ISO 8601 datetime
- Task owners are validated against .claude/agents/engineers/ or "main-agent"
- File written to correct path: project/v{version}/release-plan/roadmap.json
