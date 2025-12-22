# Phase Creator Script

CLI tool to manage phases, milestones, and tasks in `project/status.json`.

## Usage

```bash
uv run .claude/scripts/phase_creator/phase_creator.py <command> <action> [options]
```

## Commands

### Add Phase

```bash
uv run .claude/scripts/phase_creator/phase_creator.py phase add \
  --id "1" \
  --name "Foundation - Environment Setup"
```

| Option | Required | Description |
|--------|----------|-------------|
| `--id` | Yes | Phase ID (e.g., "1", "2") |
| `--name` | Yes | Phase name |

### Add Milestone

```bash
uv run .claude/scripts/phase_creator/phase_creator.py milestone add \
  --phase "1" \
  --id "MS-001" \
  --name "Environment Setup" \
  --goal "Next.js 15 + React 19 fully configured" \
  --parallel \
  --parallel-with "MS-002" "MS-003" \
  --dependencies "MS-000"
```

| Option | Required | Description |
|--------|----------|-------------|
| `--phase` | Yes | Parent phase ID |
| `--id` | Yes | Milestone ID (e.g., "MS-001") |
| `--name` | Yes | Milestone name |
| `--goal` | Yes | Milestone goal description |
| `--parallel` | No | Enable parallel execution |
| `--parallel-with` | No | Milestone IDs to run in parallel with |
| `--dependencies` | No | Milestone IDs this depends on |

### Add Task

```bash
uv run .claude/scripts/phase_creator/phase_creator.py task add \
  --phase "1" \
  --milestone "MS-001" \
  --id "T001" \
  --description "Initialize Next.js 15.1 project" \
  --priority \
  --subagent-delegation \
  --subagents fullstack-developer test-engineer \
  --dependencies "T000"
```

| Option | Required | Description |
|--------|----------|-------------|
| `--phase` | Yes | Parent phase ID |
| `--milestone` | Yes | Parent milestone ID |
| `--id` | Yes | Task ID (e.g., "T001") |
| `--description` | Yes | Task description |
| `--priority` | No | Mark as critical path task |
| `--subagent-delegation` | No | Enable subagent delegation |
| `--subagents` | No* | Subagents to use (*required if `--subagent-delegation` set) |
| `--dependencies` | No | Task IDs this depends on |

**Available Subagents** (from `.claude/agents/engineers/`):
- `fullstack-developer`
- `test-engineer`

### Add Acceptance Criteria

```bash
uv run .claude/scripts/phase_creator/phase_creator.py criteria add \
  --phase "1" \
  --milestone "MS-001" \
  --id "AC-001" \
  --description "npm run dev starts without errors"
```

| Option | Required | Description |
|--------|----------|-------------|
| `--phase` | Yes | Parent phase ID |
| `--milestone` | Yes | Parent milestone ID |
| `--id` | Yes | Criteria ID (e.g., "AC-001") |
| `--description` | Yes | Criteria description |

## Output

- **Success**: JSON with added item details
- **Error**: Error message to stderr, exit code 1

## Validation

- Phase IDs must be unique
- Milestone IDs must be unique within project
- Task IDs must be unique within milestone
- AC IDs must be unique within milestone
- Subagents validated against `.claude/agents/engineers/`
- `--parallel-with` and `--dependencies` for milestones:
  - Must match `MS-NNN` format (e.g., `MS-001`, `MS-002`)
  - Referenced milestones must exist
- Summary counts auto-updated after each operation
- `metadata.last_updated` updated on every change
