# Scripts Directory

## Purpose

Automation scripts for Claude Code workflow and session management.

## Available Scripts

### Claude Launch Scripts

#### 1. launch-new-claude.sh

**Purpose**: Start a new Claude Code session

```bash
./scripts/launch-new-claude.sh
```

#### 2. launch-resume-claude.sh

**Purpose**: Resume an existing Claude Code session

```bash
./scripts/launch-resume-claude.sh
```

#### 3. launch-new-claude-yolo.sh

**Purpose**: Start Claude with auto-yes mode (skips permission prompts)

```bash
./scripts/launch-new-claude-yolo.sh
```

#### 4. launch-resume-claude-yolo.sh

**Purpose**: Resume Claude session with auto-yes mode

```bash
./scripts/launch-resume-claude-yolo.sh
```

### Multi-Session Scripts

#### 5. tmux-claude-sessions.py

**Purpose**: Spawn multiple tmux terminals for parallel Claude Code sessions

```bash
# Basic usage - spawn 2 Claude sessions as panes
python3 .claude/scripts/tmux-claude-sessions.py

# Spawn 3 sessions with tiled layout
python3 .claude/scripts/tmux-claude-sessions.py -n 3

# Spawn 4 sessions and attach immediately
python3 .claude/scripts/tmux-claude-sessions.py -n 4 --attach

# Use a specific pane layout
python3 .claude/scripts/tmux-claude-sessions.py -n 2 -l even-horizontal

# Use separate full-screen windows instead of panes
python3 .claude/scripts/tmux-claude-sessions.py -n 3 -w --attach
```

**Options**:

- `-n, --num-panes` - Number of panes/windows to spawn (default: 2)
- `-s, --session-name` - Tmux session name (default: claude-multi)
- `-l, --layout` - Pane layout: tiled, even-horizontal, even-vertical, main-horizontal, main-vertical
- `-w, --windows` - Use separate full-screen windows instead of panes
- `-p, --prefix` - Custom prefix key (e.g., `C-a`, `C-Space`). Default: `C-b`
- `-d, --working-dir` - Working directory for sessions
- `-c, --command` - Command to run in each pane (default: claude)
- `-a, --attach` - Attach to session after creating
- `-k, --kill` - Kill existing session
- `-f, --force` - Force recreate session
- `--no-run` - Create empty shells without running command
- `--list` - List all tmux sessions

**Navigation** (default prefix `Ctrl+b`, customizable with `-p`):

- Panes: Click with mouse or `PREFIX` then arrow keys
- Windows: `PREFIX` then `0-9` or `n`/`p` for next/previous
- Detach: `PREFIX` then `d`

**Requirements**: tmux must be installed (`sudo apt install tmux`)

### Setup Scripts

#### 6. setup-yolo-aliases.sh

**Purpose**: Configure shell aliases for quick Claude commands

```bash
source ./scripts/setup-yolo-aliases.sh
```

Adds the following aliases:

- `yolo` - Run Claude with `--dangerously-skip-permissions`
- `yolo-r` - Resume Claude with auto-yes mode
- Additional worktree navigation shortcuts

## Integration with Development Container

These scripts are integrated with the development container through `.devcontainer/init-shortcuts.sh`, which automatically sets up:

- YOLO aliases for quick Claude operations
- Git worktree navigation functions
- Shell shortcuts for common tasks

## Prerequisites

- Bash shell
- Python 3 (for Python scripts)
- Claude CLI installed and configured
- Git (for worktree scripts)
- tmux (for multi-session scripts)

## Usage Notes

### YOLO Mode

The YOLO (You Only Launch Once) variants automatically accept all permission prompts, useful for:

- Automated workflows
- Experienced users who understand the risks
- Development environments where permissions are pre-approved

⚠️ **Warning**: YOLO mode skips safety prompts. Use with caution in production environments.

### Session Management

- New sessions start fresh with no prior context
- Resume sessions continue from the last saved state
- Sessions are automatically saved when Claude exits normally

## Troubleshooting

If scripts fail to execute:

1. Ensure execute permissions: `chmod +x scripts/*.sh`
2. Verify Claude CLI is installed: `which claude`
3. Check shell compatibility (scripts require Bash)

---

_Last updated: 2025-12-14_
