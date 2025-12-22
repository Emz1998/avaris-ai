# Roadmap JSON Schema

**Version:** 1.0.0

This document defines the structure for `roadmap.json` files used in project execution tracking.

---

## Top-Level Structure

```json
{
  "name": "string",
  "version": "string",
  "target_release": "string (ISO date)",
  "status": "string",
  "phases": [],
  "summary": {},
  "metadata": {}
}
```

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Project name |
| `version` | string | Version being tracked (e.g., "0.1.0") |
| `target_release` | string | Target release date (ISO format) |
| `status` | string | Overall status: `not_started`, `in_progress`, `completed` |
| `phases` | array | Sequential execution phases |
| `summary` | object | Computed counts for phases, milestones, tasks |
| `metadata` | object | Schema version and last update timestamp |

---

## Phase

Phases run **sequentially**. Order in array determines execution order.

```json
{
  "id": "PH-NNN",
  "name": "string",
  "status": "string",
  "milestones": []
}
```

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier (pattern: `PH-NNN`) |
| `name` | string | Phase name |
| `status` | string | `not_started`, `in_progress`, `completed` |
| `milestones` | array | Milestones within this phase (run in parallel) |

---

## Milestone

Milestones within a phase run **in parallel**. One feature per milestone (1:1 mapping).

```json
{
  "id": "MS-NNN",
  "feature": "FNNN",
  "name": "string",
  "goal": "string",
  "status": "string",
  "dependencies": [],
  "success_criteria": [],
  "tasks": []
}
```

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier (pattern: `MS-NNN`) |
| `feature` | string | Reference to feature in product.json (pattern: `FNNN`) |
| `name` | string | Milestone name |
| `goal` | string | What this milestone achieves |
| `status` | string | `not_started`, `in_progress`, `completed` |
| `dependencies` | array | MS-IDs that must complete first |
| `success_criteria` | array | Feature-level success verification |
| `tasks` | array | Tasks to complete this milestone |

---

## Success Criteria (Milestone Level)

References SC from product.json. Verifies feature-level outcomes.

```json
{
  "references": ["SC-NNN"],
  "met": false
}
```

| Field | Type | Description |
|-------|------|-------------|
| `references` | array | SC-IDs from product.json |
| `met` | boolean | Whether criteria has been verified |

---

## Task

Individual work items that satisfy acceptance criteria.

```json
{
  "id": "TNNN",
  "description": "string",
  "status": "string",
  "parallel": false,
  "owner": "string",
  "dependencies": [],
  "acceptance_criteria": []
}
```

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier (pattern: `TNNN`) |
| `description` | string | What the task accomplishes |
| `status` | string | `not_started`, `in_progress`, `completed` |
| `parallel` | boolean | Can run in parallel with other tasks |
| `owner` | string | Agent responsible (from `.claude/agents/engineers/` or `main-agent`) |
| `dependencies` | array | T-IDs that must complete first |
| `acceptance_criteria` | array | AC references from product.json |

---

## Acceptance Criteria (Task Level)

References AC from product.json. Verifies user story behaviors.

```json
{
  "references": ["AC-NNN"],
  "met": false
}
```

| Field | Type | Description |
|-------|------|-------------|
| `references` | array | AC-IDs from product.json user stories |
| `met` | boolean | Whether criteria has been satisfied |

---

## Summary

Computed counts updated after every mutation.

```json
{
  "phases": {
    "total": 0,
    "pending": 0,
    "completed": 0,
    "recently_completed": "",
    "current_phase": ""
  },
  "milestones": {
    "total": 0,
    "pending": 0,
    "completed": 0,
    "recently_completed": "",
    "current_milestone": ""
  },
  "tasks": {
    "total": 0,
    "pending": 0,
    "completed": 0,
    "recently_completed": "",
    "current_task": ""
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `total` | number | Total count |
| `pending` | number | Count where status != `completed` |
| `completed` | number | Count where status == `completed` |
| `recently_completed` | string | ID of most recently completed item |
| `current_*` | string | ID of item currently `in_progress` |

---

## Metadata

```json
{
  "last_updated": "ISO 8601 datetime",
  "schema_version": "1.0.0"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `last_updated` | string | Last modification timestamp |
| `schema_version` | string | Schema version for compatibility |

---

## ID Patterns

| Entity | Pattern | Example |
|--------|---------|---------|
| Phase | `PH-NNN` | PH-001 |
| Milestone | `MS-NNN` | MS-001 |
| Task | `TNNN` | T001 |
| Success Criteria | `SC-NNN` | SC-001 (from product.json) |
| Acceptance Criteria | `AC-NNN` | AC-001 (from product.json) |
| Feature | `FNNN` | F001 (from product.json) |

---

## Relationships

```
product.json                    roadmap.json
──────────────────────────────────────────────────
Feature (FNNN)            →     Milestone (MS-NNN)
  └─ SC (SC-NNN)          →       └─ success_criteria.references
  └─ User Story (US-NNN)
       └─ AC (AC-NNN)     →     Task (TNNN)
                                  └─ acceptance_criteria.references
```

---

## Completion Logic

| Level | Complete When |
|-------|---------------|
| Task | status = `completed` AND all acceptance_criteria.met = true |
| Milestone | All tasks complete AND all success_criteria.met = true |
| Phase | All milestones complete |
| Roadmap | All phases complete |

---

## Status Values

| Value | Meaning |
|-------|---------|
| `not_started` | Work has not begun |
| `in_progress` | Currently being worked on |
| `completed` | Work finished and verified |
