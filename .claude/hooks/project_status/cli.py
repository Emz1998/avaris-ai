"""
CLI for project status updates with auto-cascade.

Usage:
    python3 cli.py <ID> --status <status> -f <file>
    python3 cli.py T001 --status completed -f status.json
    python3 cli.py MS-001 --status completed -f status.json
    python3 cli.py prd --status completed -f status.json
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

# Handle both direct execution and module import
try:
    from .project_status import ProjectStatusManager
    from .schema import SpecStatusEnum, StatusEnum
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent))
    from project_status import ProjectStatusManager  # type: ignore[import-not-found,no-redef]
    from schema import SpecStatusEnum, StatusEnum  # type: ignore[import-not-found,no-redef]


DEFAULT_STATUS_FILE = "./project/status.json"


@dataclass
class TargetLocation:
    """Location of a target item."""

    phase_key: Optional[str] = None
    milestone_id: Optional[str] = None
    task_id: Optional[str] = None
    ac_id: Optional[str] = None


class TargetType:
    """Target type constants."""

    PROJECT = "project"
    SPEC = "spec"
    PHASE = "phase"
    MILESTONE = "milestone"
    TASK = "task"
    AC = "ac"
    CURRENT = "current"


def detect_target_type(target_id: str) -> tuple[str, str]:
    """Detect target type from ID pattern. Returns (type, normalized_id)."""
    target_id = target_id.strip()

    if target_id.lower() == "project":
        return TargetType.PROJECT, target_id

    if target_id.lower() in ("prd", "tech", "ux"):
        return TargetType.SPEC, target_id.lower()

    if target_id.lower() == "current":
        return TargetType.CURRENT, target_id

    if re.match(r"^T\d{3}$", target_id, re.IGNORECASE):
        return TargetType.TASK, target_id.upper()

    if re.match(r"^MS-\d{3}$", target_id, re.IGNORECASE):
        return TargetType.MILESTONE, target_id.upper()

    if re.match(r"^AC-\d{3}$", target_id, re.IGNORECASE):
        return TargetType.AC, target_id.upper()

    if re.match(r"^\d+$", target_id):
        return TargetType.PHASE, target_id

    raise ValueError(f"Unknown target ID pattern: {target_id}")


class StatusUpdater:
    """Handles status updates with auto-cascade."""

    def __init__(self, manager: ProjectStatusManager, no_cascade: bool = False) -> None:
        self._manager = manager
        self._no_cascade = no_cascade
        self._messages: list[str] = []

    def _log(self, msg: str) -> None:
        self._messages.append(msg)

    def get_messages(self) -> list[str]:
        return self._messages

    def find_task(self, task_id: str) -> Optional[TargetLocation]:
        """Find task location by ID."""
        for phase_key, phase in self._manager.list_phases().items():
            for ms_id, milestone in phase.milestones.items():
                if task_id in milestone.tasks:
                    return TargetLocation(
                        phase_key=phase_key,
                        milestone_id=ms_id,
                        task_id=task_id,
                    )
        return None

    def find_milestone(self, milestone_id: str) -> Optional[TargetLocation]:
        """Find milestone location by ID."""
        for phase_key, phase in self._manager.list_phases().items():
            if milestone_id in phase.milestones:
                return TargetLocation(
                    phase_key=phase_key,
                    milestone_id=milestone_id,
                )
        return None

    def find_ac(self, ac_id: str) -> Optional[TargetLocation]:
        """Find acceptance criteria location by ID."""
        for phase_key, phase in self._manager.list_phases().items():
            for ms_id, milestone in phase.milestones.items():
                for ac in milestone.acceptance_criteria:
                    if ac.id == ac_id:
                        return TargetLocation(
                            phase_key=phase_key,
                            milestone_id=ms_id,
                            ac_id=ac_id,
                        )
        return None

    def update_project(self, status: StatusEnum) -> None:
        """Update project status."""
        self._manager.project_status = status
        self._log(f"project -> {status.value}")

    def update_spec(self, spec_type: str, status: SpecStatusEnum) -> None:
        """Update spec status."""
        self._manager.set_spec_status(spec_type, status)
        self._log(f"{spec_type} -> {status.value}")

    def update_phase(self, phase_key: str, status: StatusEnum) -> None:
        """Update phase status."""
        phase = self._manager.get_phase(phase_key)
        if not phase:
            raise KeyError(f"Phase {phase_key} not found")
        self._manager.set_phase_status(phase_key, status)
        self._log(f"phase {phase_key} -> {status.value}")

    def update_milestone(
        self, phase_key: str, milestone_id: str, status: StatusEnum
    ) -> None:
        """Update milestone status with optional cascade to phase."""
        self._manager.set_milestone_status(phase_key, milestone_id, status)
        self._log(f"{milestone_id} -> {status.value}")

        if self._no_cascade:
            return

        if status == StatusEnum.COMPLETED:
            self._cascade_to_phase(phase_key)
        else:
            self._reverse_cascade_phase(phase_key)

    def update_task(
        self,
        phase_key: str,
        milestone_id: str,
        task_id: str,
        status: StatusEnum,
    ) -> None:
        """Update task status with optional cascade to milestone and phase."""
        self._manager.set_task_status(phase_key, milestone_id, task_id, status)
        self._log(f"{task_id} -> {status.value}")

        if self._no_cascade:
            return

        if status == StatusEnum.COMPLETED:
            self._cascade_to_milestone(phase_key, milestone_id)
        else:
            self._reverse_cascade_milestone(phase_key, milestone_id)

    def update_ac(
        self, phase_key: str, milestone_id: str, ac_id: str, met: bool
    ) -> None:
        """Update acceptance criteria met status."""
        self._manager.set_acceptance_criteria_met(phase_key, milestone_id, ac_id, met)
        self._log(f"{ac_id} -> met={met}")

    def update_current(
        self,
        phase: Optional[str],
        milestone: Optional[str],
        task: Optional[str],
    ) -> None:
        """Update current work context."""
        self._manager.set_current(phase, milestone, task)
        parts = []
        if phase:
            parts.append(f"phase {phase}")
        if milestone:
            parts.append(milestone)
        if task:
            parts.append(task)
        self._log(f"current -> {' > '.join(parts) if parts else 'cleared'}")

    def _cascade_to_milestone(self, phase_key: str, milestone_id: str) -> None:
        """Update milestone status based on task states."""
        tasks = self._manager.list_tasks(phase_key, milestone_id)
        milestone = self._manager.get_milestone(phase_key, milestone_id)
        if not tasks or not milestone:
            return

        all_completed = all(t.status == StatusEnum.COMPLETED for t in tasks.values())

        if all_completed:
            if milestone.status != StatusEnum.COMPLETED:
                self._manager.set_milestone_status(
                    phase_key, milestone_id, StatusEnum.COMPLETED
                )
                self._log(f"{milestone_id} -> completed (auto)")
                self._cascade_to_phase(phase_key)
        elif milestone.status == StatusEnum.NOT_STARTED:
            self._manager.set_milestone_status(
                phase_key, milestone_id, StatusEnum.IN_PROGRESS
            )
            self._log(f"{milestone_id} -> in_progress (auto)")
            self._cascade_to_phase_in_progress(phase_key)

    def _cascade_to_phase(self, phase_key: str) -> None:
        """Check if all milestones complete, then complete phase."""
        milestones = self._manager.list_milestones(phase_key)
        if not milestones:
            return

        all_completed = all(
            m.status == StatusEnum.COMPLETED for m in milestones.values()
        )
        if all_completed:
            phase = self._manager.get_phase(phase_key)
            if phase and phase.status != StatusEnum.COMPLETED:
                self._manager.set_phase_status(phase_key, StatusEnum.COMPLETED)
                self._log(f"phase {phase_key} -> completed (auto)")

    def _cascade_to_phase_in_progress(self, phase_key: str) -> None:
        """Set phase to in_progress if it was not_started."""
        phase = self._manager.get_phase(phase_key)
        if phase and phase.status == StatusEnum.NOT_STARTED:
            self._manager.set_phase_status(phase_key, StatusEnum.IN_PROGRESS)
            self._log(f"phase {phase_key} -> in_progress (auto)")

    def _reverse_cascade_milestone(self, phase_key: str, milestone_id: str) -> None:
        """Revert milestone/phase status when a task is no longer completed."""
        tasks = self._manager.list_tasks(phase_key, milestone_id)
        milestone = self._manager.get_milestone(phase_key, milestone_id)
        if not milestone:
            return

        all_not_started = all(
            t.status == StatusEnum.NOT_STARTED for t in tasks.values()
        )
        new_status = (
            StatusEnum.NOT_STARTED if all_not_started else StatusEnum.IN_PROGRESS
        )

        if milestone.status != new_status:
            self._manager.set_milestone_status(phase_key, milestone_id, new_status)
            self._log(f"{milestone_id} -> {new_status.value} (auto)")
            self._reverse_cascade_phase(phase_key)

    def _reverse_cascade_phase(self, phase_key: str) -> None:
        """Revert phase status when a milestone is no longer completed."""
        milestones = self._manager.list_milestones(phase_key)
        phase = self._manager.get_phase(phase_key)
        if not phase:
            return

        all_not_started = all(
            m.status == StatusEnum.NOT_STARTED for m in milestones.values()
        )
        new_status = (
            StatusEnum.NOT_STARTED if all_not_started else StatusEnum.IN_PROGRESS
        )

        if phase.status != new_status:
            self._manager.set_phase_status(phase_key, new_status)
            self._log(f"phase {phase_key} -> {new_status.value} (auto)")


def build_parser() -> argparse.ArgumentParser:
    """Build argument parser."""
    parser = argparse.ArgumentParser(
        prog="project-status",
        description="Update project status with auto-cascade",
    )
    parser.add_argument(
        "target",
        help="Target ID (T001, MS-001, 1, prd, project, current)",
    )
    parser.add_argument(
        "--file",
        "-f",
        default=DEFAULT_STATUS_FILE,
        help=f"Path to status.json (default: {DEFAULT_STATUS_FILE})",
    )
    parser.add_argument(
        "--status",
        "-s",
        choices=["not_started", "in_progress", "completed", "blocked"],
        help="Status value",
    )
    parser.add_argument(
        "--met",
        choices=["true", "false"],
        help="AC met status (true/false)",
    )
    parser.add_argument(
        "--no-cascade",
        action="store_true",
        help="Disable auto-cascade",
    )
    parser.add_argument(
        "--phase",
        "-p",
        help="Phase for current command",
    )
    parser.add_argument(
        "--milestone",
        "-m",
        help="Milestone for current command",
    )
    parser.add_argument(
        "--task",
        "-t",
        help="Task for current command",
    )
    return parser


def run(args: argparse.Namespace) -> int:
    """Execute the command."""
    file_path = Path(args.file)
    if not file_path.exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        return 1

    manager = ProjectStatusManager(file_path)
    manager.load()

    updater = StatusUpdater(manager, no_cascade=args.no_cascade)

    try:
        target_type, target_id = detect_target_type(args.target)

        if target_type == TargetType.PROJECT:
            if not args.status:
                print("Error: --status required", file=sys.stderr)
                return 1
            updater.update_project(StatusEnum(args.status))

        elif target_type == TargetType.SPEC:
            if not args.status:
                print("Error: --status required", file=sys.stderr)
                return 1
            updater.update_spec(target_id, SpecStatusEnum(args.status))

        elif target_type == TargetType.PHASE:
            if not args.status:
                print("Error: --status required", file=sys.stderr)
                return 1
            updater.update_phase(target_id, StatusEnum(args.status))

        elif target_type == TargetType.MILESTONE:
            if not args.status:
                print("Error: --status required", file=sys.stderr)
                return 1
            loc = updater.find_milestone(target_id)
            if not loc or not loc.phase_key:
                print(f"Error: Milestone {target_id} not found", file=sys.stderr)
                return 1
            updater.update_milestone(loc.phase_key, target_id, StatusEnum(args.status))

        elif target_type == TargetType.TASK:
            if not args.status:
                print("Error: --status required", file=sys.stderr)
                return 1
            loc = updater.find_task(target_id)
            if not loc or not loc.phase_key or not loc.milestone_id:
                print(f"Error: Task {target_id} not found", file=sys.stderr)
                return 1
            updater.update_task(
                loc.phase_key, loc.milestone_id, target_id, StatusEnum(args.status)
            )

        elif target_type == TargetType.AC:
            if not args.met:
                print("Error: --met required for AC", file=sys.stderr)
                return 1
            loc = updater.find_ac(target_id)
            if not loc or not loc.phase_key or not loc.milestone_id:
                print(f"Error: AC {target_id} not found", file=sys.stderr)
                return 1
            updater.update_ac(
                loc.phase_key, loc.milestone_id, target_id, args.met == "true"
            )

        elif target_type == TargetType.CURRENT:
            updater.update_current(args.phase, args.milestone, args.task)

        manager.recalculate_summary()
        manager.save()

        for msg in updater.get_messages():
            print(f"  {msg}")

        return 0

    except KeyError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def main() -> int:
    """CLI entry point."""
    parser = build_parser()
    args = parser.parse_args()
    return run(args)


if __name__ == "__main__":
    sys.exit(main())
