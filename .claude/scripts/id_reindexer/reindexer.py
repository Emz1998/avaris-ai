#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "watchdog>=4.0.0",
# ]
# ///
"""
Auto-reindex IDs in status.json when order changes.

Uses watchdog to monitor the file and automatically update IDs based on index:
- Phases: PHASE-001, PHASE-002, etc.
- Milestones: MS-001, MS-002, etc.
- Tasks: T001, T002, etc.

Usage:
    uv run .claude/scripts/id_reindexer/reindexer.py
"""

import json
import time
import sys
from pathlib import Path
from datetime import datetime, timezone
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

STATUS_FILE = Path(__file__).parent.parent.parent.parent / "project" / "status.json"


def generate_phase_id(index: int) -> str:
    """Generate phase ID from index (0-based -> PHASE-001)."""
    return f"PHASE-{index + 1:03d}"


def generate_milestone_id(index: int) -> str:
    """Generate milestone ID from index (0-based -> MS-001)."""
    return f"MS-{index + 1:03d}"


def generate_task_id(index: int) -> str:
    """Generate task ID from index (0-based -> T001)."""
    return f"T{index + 1:03d}"


def reindex_status(data: dict) -> tuple[dict, bool]:
    """
    Reindex all IDs in the status data based on current positions.

    Returns:
        tuple: (updated_data, was_changed)
    """
    changed = False

    phases = data.get("phases", [])

    for phase_idx, phase in enumerate(phases):
        # Reindex phase ID
        expected_phase_id = generate_phase_id(phase_idx)
        if phase.get("id") != expected_phase_id:
            print(f"  Phase: {phase.get('id')} -> {expected_phase_id}", flush=True)
            phase["id"] = expected_phase_id
            changed = True

        # Reindex milestones within this phase
        milestones = phase.get("milestones", [])
        for ms_idx, milestone in enumerate(milestones):
            expected_ms_id = generate_milestone_id(ms_idx)
            if milestone.get("id") != expected_ms_id:
                print(f"  Milestone: {milestone.get('id')} -> {expected_ms_id}", flush=True)
                milestone["id"] = expected_ms_id
                changed = True

            # Reindex tasks within this milestone
            tasks = milestone.get("tasks", [])
            for task_idx, task in enumerate(tasks):
                expected_task_id = generate_task_id(task_idx)
                if task.get("id") != expected_task_id:
                    print(f"  Task: {task.get('id')} -> {expected_task_id}", flush=True)
                    task["id"] = expected_task_id
                    changed = True

    return data, changed


def process_file(filepath: Path) -> None:
    """Read, reindex, and write back the status file if changes detected."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        updated_data, changed = reindex_status(data)

        if changed:
            # Update metadata timestamp
            if "metadata" in updated_data:
                updated_data["metadata"]["last_updated"] = datetime.now(timezone.utc).isoformat()

            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(updated_data, f, indent=2, ensure_ascii=False)

            print(f"[{datetime.now().strftime('%H:%M:%S')}] IDs reindexed successfully", flush=True)
        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] No reindexing needed", flush=True)

    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {filepath}: {e}", flush=True)
    except Exception as e:
        print(f"Error processing {filepath}: {e}", flush=True)


class StatusFileHandler(FileSystemEventHandler):
    """Handler for status.json file changes."""

    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.last_processed = 0
        self.debounce_seconds = 0.5  # Prevent rapid re-processing
        self._processing = False

    def on_modified(self, event):
        if event.is_directory:
            return

        # Check if it's our target file
        if Path(event.src_path).resolve() != self.filepath.resolve():
            return

        # Debounce to avoid processing multiple times
        current_time = time.time()
        if current_time - self.last_processed < self.debounce_seconds:
            return

        # Prevent recursive processing
        if self._processing:
            return

        self._processing = True
        self.last_processed = current_time

        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Change detected in status.json", flush=True)

        # Small delay to ensure file write is complete
        time.sleep(0.1)

        process_file(self.filepath)
        self._processing = False


def main():
    """Main entry point - start watching the status file."""
    if not STATUS_FILE.exists():
        print(f"Error: Status file not found at {STATUS_FILE}", flush=True)
        sys.exit(1)

    print(f"Watching: {STATUS_FILE}", flush=True)
    print("Press Ctrl+C to stop\n", flush=True)

    # Process once on startup
    print("Initial check:", flush=True)
    process_file(STATUS_FILE)

    # Set up watchdog observer
    event_handler = StatusFileHandler(STATUS_FILE)
    observer = Observer()
    observer.schedule(event_handler, str(STATUS_FILE.parent), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping watcher...", flush=True)
        observer.stop()

    observer.join()
    print("Watcher stopped.", flush=True)


if __name__ == "__main__":
    main()
