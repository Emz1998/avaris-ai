# Project Status CLI

A CLI tool for tracking project progress with auto-cascade status updates.

## Installation

Requires Python 3.10+ and Pydantic.

```bash
pip install pydantic
```

## Usage

```bash
python3 cli.py <ID> --status <status> -f <file>
```

## Commands

### Task

```bash
python3 cli.py T001 -s completed -f status.json
python3 cli.py T001 -s in_progress -f status.json
python3 cli.py T001 -s not_started -f status.json
```

### Milestone

```bash
python3 cli.py MS-001 -s completed -f status.json
```

### Phase

```bash
python3 cli.py 1 -s completed -f status.json
```

### Specs (prd, tech, ux)

```bash
python3 cli.py prd -s completed -f status.json
python3 cli.py tech -s in_progress -f status.json
python3 cli.py ux -s not_started -f status.json
```

### Project

```bash
python3 cli.py project -s in_progress -f status.json
```

### Acceptance Criteria

```bash
python3 cli.py AC-001 --met true -f status.json
python3 cli.py AC-001 --met false -f status.json
```

### Current Work Context

```bash
python3 cli.py current -p 1 -m MS-001 -t T001 -f status.json
```

## Options

| Option         | Short | Description                   |
| -------------- | ----- | ----------------------------- |
| `--file`       | `-f`  | Path to status.json           |
| `--status`     | `-s`  | Status value                  |
| `--met`        |       | AC met status (true/false)    |
| `--phase`      | `-p`  | Phase for current command     |
| `--milestone`  | `-m`  | Milestone for current command |
| `--task`       | `-t`  | Task for current command      |
| `--no-cascade` |       | Disable auto-cascade          |

## Status Values

- `not_started`
- `in_progress`
- `completed`
- `blocked`

## Auto-Cascade

When a task status changes, parent milestones and phases update automatically:

**Forward cascade (completing):**

```
T001 -> completed
T002 -> completed
  -> MS-001 -> completed (all tasks done)
  -> phase 1 -> completed (all milestones done)
```

**Reverse cascade (reverting):**

```
T001 -> not_started
  -> MS-001 -> in_progress (or not_started if all tasks not_started)
  -> phase 1 -> in_progress (or not_started if all milestones not_started)
```

Use `--no-cascade` to disable this behavior.

## ID Patterns

| Pattern       | Example        | Target              |
| ------------- | -------------- | ------------------- |
| `T###`        | T001, T050     | Task                |
| `MS-###`      | MS-001, MS-020 | Milestone           |
| `#`           | 1, 2, 3        | Phase               |
| `AC-###`      | AC-001         | Acceptance Criteria |
| `prd/tech/ux` | prd            | Spec                |
| `project`     | project        | Project             |
| `current`     | current        | Current context     |

## Files

- `schema.py` - Pydantic models for status.json
- `project_status.py` - ProjectStatusManager class
- `cli.py` - CLI entry point
