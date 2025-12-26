---
name: project-management
description: Creates and manages project roadmap.json files with phases, milestones, and tasks. Use when creating roadmaps, adding phases/milestones/tasks, updating status, or when user mentions roadmap management, release planning, or project phases.
---

**Goal**: Create and maintain structured roadmap.json files in `project/v{version}/release-plan/roadmap.json` that track project phases, milestones, and tasks.

**IMPORTANT**: Phases run SEQUENTIALLY. Milestones within a phase run in PARALLEL. If a milestone must run sequentially, place it in its own single-milestone phase.

## Workflow

### Phase 1: Assessment

1. Read `project/status.json` to get current version
2. Construct target path: `project/v{version}/release-plan/roadmap.json`
3. Check if roadmap.json exists (determines create vs update)
4. Read `.claude/skills/project-management/references/schema.json` for schema reference
5. **Read specs for context** (required for create/add operations):
   - `project/product/PRD.md` - Product requirements, features, user stories
   - `project/v{version}/specs/tech-specs.md` - Architecture, data models, APIs
   - `project/v{version}/specs/ui-ux.md` - UI components, user flows

### Phase 2: Operation Execution

**Create roadmap:**

- Analyze specs to derive phases, milestones, and tasks
- Extract features from PRD, map to milestones via `feature` field (e.g., "F001")
- Extract technical requirements from tech-specs, create tasks with owners
- Extract UI components from ux.md, create tasks for UI development
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
- Create milestone with `feature` field linking to PRD feature (e.g., "F001")
- Create empty tasks array and success_criteria array
- Append to phase.milestones

**Add task:**

- Find target milestone by MS-ID
- Validate owner against `.claude/agents/engineers/` folder or "main-agent"
- Generate next T-ID
- Set `parallel` field (true if task can run in parallel, false if sequential)
- Create empty acceptance_criteria array
- Append to milestone.tasks

**Update status:**

- Find item by ID (PH-xxx, MS-xxx, or Txxx)
- Update status field to "not_started", "in_progress", or "completed"

**Mark criteria met:**

- Find criteria by id_reference (SC-xxx or AC-xxx)
- Set status to "met" or "unmet"

### Phase 3: Finalization

1. Recompute summary section:
   - Count totals, pending (status != completed), completed for phases, milestones, tasks
2. Update `current` section with active phase, milestone, and task IDs
3. Update `metadata.last_updated` to current ISO 8601 datetime
4. Write to target roadmap.json file
5. Report changes made

## Rules

- **MUST** read specs (prd.md, tech-specs.md, ux.md) before creating or adding to roadmap
- **ID Generation**: Scan all existing IDs of type, find max numeric value, increment by 1, pad to 3 digits
- **ID Patterns**: PH-NNN (phases), MS-NNN (milestones), TNNN (tasks), SC-NNN (success criteria), AC-NNN (acceptance criteria)
- **Feature References**: Milestones should reference features from PRD using format "F001", "F002", etc.
- **Valid owners**: Any subagents (without .md) in `.claude/agents/engineers/`
- **Valid status values**: "not_started", "in_progress", "completed"
- **Valid criteria status**: "met", "unmet"
- **Milestone dependencies**: Must reference existing MS-IDs from same or previous phases
- **Task dependencies**: Must reference existing T-IDs within the same milestone
- **Task parallel field**: Set to true for tasks that can run in parallel, false for sequential
- **NEVER** modify phases array order (order determines sequential execution)
- **MUST** recompute summary after every mutation
- **MUST** update metadata.last_updated after every mutation
- **MUST** update current section with active IDs after every mutation

## Schema Reference

See [references/schema.json](references/schema.json) for complete JSON structure.

## Acceptance Criteria

- Roadmap.json follows exact structure from schema.json
- All IDs follow correct patterns (PH-NNN, MS-NNN, TNNN, SC-NNN, AC-NNN)
- Feature references in milestones match PRD feature IDs
- Success criteria use `id_reference` and `status` fields
- Acceptance criteria use `id_reference` and `status` fields
- Task `parallel` field is set correctly based on dependencies
- Summary section accurately reflects current counts
- Current section contains active phase, milestone, and task IDs
- metadata.last_updated is current ISO 8601 datetime
- Task owners are validated against .claude/agents/engineers/
- File written to correct path: project/v{version}/release-plan/roadmap.json
