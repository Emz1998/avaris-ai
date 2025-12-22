"""
ProjectStatus manager class for accessing and modifying project status data.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# Handle both direct execution and module import
try:
    from .schema import (
        AcceptanceCriteria,
        Metadata,
        Milestone,
        Phase,
        Project,
        ProjectStatus,
        SpecStatusEnum,
        StatusEnum,
        Task,
    )
except ImportError:
    from schema import (  # type: ignore[import-not-found,no-redef]
        AcceptanceCriteria,
        Metadata,
        Milestone,
        Phase,
        Project,
        ProjectStatus,
        SpecStatusEnum,
        StatusEnum,
        Task,
    )


class ProjectStatusManager:
    """Manager class for project status data with getters and setters."""

    def __init__(self, file_path: Optional[str | Path] = None) -> None:
        self._file_path: Optional[Path] = Path(file_path) if file_path else None
        self._data: Optional[ProjectStatus] = None

    # --- File Operations ---

    def load(self, file_path: Optional[str | Path] = None) -> ProjectStatusManager:
        """Load status from JSON file."""
        path = Path(file_path) if file_path else self._file_path
        if not path:
            raise ValueError("No file path specified")
        self._file_path = path
        with open(path, "r", encoding="utf-8") as f:
            self._data = ProjectStatus.model_validate(json.load(f))
        return self

    def save(self, file_path: Optional[str | Path] = None) -> None:
        """Save status to JSON file."""
        path = Path(file_path) if file_path else self._file_path
        if not path:
            raise ValueError("No file path specified")
        if not self._data:
            raise ValueError("No data to save")
        self._touch_metadata()
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self._data.model_dump(mode="json"), f, indent=2, default=str)

    def _touch_metadata(self) -> None:
        """Update last_updated timestamp."""
        if self._data:
            self._data.metadata.last_updated = datetime.now(timezone.utc)

    def _ensure_data(self) -> ProjectStatus:
        """Ensure data is loaded."""
        if not self._data:
            raise ValueError("No data loaded. Call load() first or use create().")
        return self._data

    # --- Factory ---

    def create(
        self,
        name: str,
        version: str = "0.1.0",
        target_release: str = "",
    ) -> ProjectStatusManager:
        """Create a new project status."""
        self._data = ProjectStatus(
            project=Project(
                name=name,
                version=version,
                target_release=target_release,
                status=StatusEnum.NOT_STARTED,
            ),
            metadata=Metadata(),
        )
        return self

    # --- Project Getters/Setters ---

    @property
    def project_name(self) -> str:
        return self._ensure_data().project.name

    @project_name.setter
    def project_name(self, value: str) -> None:
        self._ensure_data().project.name = value

    @property
    def project_version(self) -> str:
        return self._ensure_data().project.version

    @project_version.setter
    def project_version(self, value: str) -> None:
        self._ensure_data().project.version = value

    @property
    def project_target_release(self) -> str:
        return self._ensure_data().project.target_release

    @project_target_release.setter
    def project_target_release(self, value: str) -> None:
        self._ensure_data().project.target_release = value

    @property
    def project_status(self) -> StatusEnum:
        return self._ensure_data().project.status

    @project_status.setter
    def project_status(self, value: StatusEnum) -> None:
        self._ensure_data().project.status = value

    # --- Specs Getters/Setters ---

    def get_spec_status(self, spec_type: str) -> SpecStatusEnum:
        """Get status of a spec (prd, tech, ux)."""
        specs = self._ensure_data().specs
        return getattr(specs, spec_type).status

    def set_spec_status(self, spec_type: str, status: SpecStatusEnum) -> None:
        """Set status of a spec (prd, tech, ux)."""
        specs = self._ensure_data().specs
        getattr(specs, spec_type).status = status

    def get_spec_path(self, spec_type: str) -> str:
        """Get path of a spec (prd, tech, ux)."""
        specs = self._ensure_data().specs
        return getattr(specs, spec_type).path

    def set_spec_path(self, spec_type: str, path: str) -> None:
        """Set path of a spec (prd, tech, ux)."""
        specs = self._ensure_data().specs
        getattr(specs, spec_type).path = path

    # --- Summary Getters/Setters ---

    @property
    def phases_total(self) -> int:
        return self._ensure_data().summary.phases.total

    @phases_total.setter
    def phases_total(self, value: int) -> None:
        self._ensure_data().summary.phases.total = value

    @property
    def phases_completed(self) -> int:
        return self._ensure_data().summary.phases.completed

    @phases_completed.setter
    def phases_completed(self, value: int) -> None:
        self._ensure_data().summary.phases.completed = value

    @property
    def milestones_total(self) -> int:
        return self._ensure_data().summary.milestones.total

    @milestones_total.setter
    def milestones_total(self, value: int) -> None:
        self._ensure_data().summary.milestones.total = value

    @property
    def milestones_completed(self) -> int:
        return self._ensure_data().summary.milestones.completed

    @milestones_completed.setter
    def milestones_completed(self, value: int) -> None:
        self._ensure_data().summary.milestones.completed = value

    @property
    def tasks_total(self) -> int:
        return self._ensure_data().summary.tasks.total

    @tasks_total.setter
    def tasks_total(self, value: int) -> None:
        self._ensure_data().summary.tasks.total = value

    @property
    def tasks_completed(self) -> int:
        return self._ensure_data().summary.tasks.completed

    @tasks_completed.setter
    def tasks_completed(self, value: int) -> None:
        self._ensure_data().summary.tasks.completed = value

    # --- Current Work Getters/Setters ---

    @property
    def current_phase(self) -> Optional[str]:
        return self._ensure_data().current.phase

    @current_phase.setter
    def current_phase(self, value: Optional[str]) -> None:
        self._ensure_data().current.phase = value

    @property
    def current_milestone(self) -> Optional[str]:
        return self._ensure_data().current.milestone

    @current_milestone.setter
    def current_milestone(self, value: Optional[str]) -> None:
        self._ensure_data().current.milestone = value

    @property
    def current_task(self) -> Optional[str]:
        return self._ensure_data().current.task

    @current_task.setter
    def current_task(self, value: Optional[str]) -> None:
        self._ensure_data().current.task = value

    def set_current(
        self,
        phase: Optional[str] = None,
        milestone: Optional[str] = None,
        task: Optional[str] = None,
    ) -> None:
        """Set current work context."""
        current = self._ensure_data().current
        current.phase = phase
        current.milestone = milestone
        current.task = task

    # --- Phase Operations ---

    def get_phase(self, phase_key: str) -> Optional[Phase]:
        """Get a phase by key (e.g., '1')."""
        return self._ensure_data().phases.get(phase_key)

    def add_phase(self, phase_key: str, phase_id: str, name: str) -> Phase:
        """Add a new phase."""
        phase = Phase(id=phase_id, name=name)
        self._ensure_data().phases[phase_key] = phase
        self.phases_total += 1
        return phase

    def set_phase_status(self, phase_key: str, status: StatusEnum) -> None:
        """Set phase status."""
        phase = self.get_phase(phase_key)
        if not phase:
            raise KeyError(f"Phase {phase_key} not found")
        if phase.status != StatusEnum.COMPLETED and status == StatusEnum.COMPLETED:
            self.phases_completed += 1
        phase.status = status

    def list_phases(self) -> dict[str, Phase]:
        """Get all phases."""
        return self._ensure_data().phases

    # --- Milestone Operations ---

    def get_milestone(self, phase_key: str, milestone_id: str) -> Optional[Milestone]:
        """Get a milestone by phase key and milestone ID."""
        phase = self.get_phase(phase_key)
        if not phase:
            return None
        return phase.milestones.get(milestone_id)

    def add_milestone(
        self,
        phase_key: str,
        milestone_id: str,
        name: str,
        goal: str,
        parallel: bool = False,
        dependencies: Optional[list[str]] = None,
    ) -> Milestone:
        """Add a milestone to a phase."""
        phase = self.get_phase(phase_key)
        if not phase:
            raise KeyError(f"Phase {phase_key} not found")
        milestone = Milestone(
            name=name,
            goal=goal,
            parallel=parallel,
            dependencies=dependencies or [],
        )
        phase.milestones[milestone_id] = milestone
        self.milestones_total += 1
        return milestone

    def set_milestone_status(
        self, phase_key: str, milestone_id: str, status: StatusEnum
    ) -> None:
        """Set milestone status."""
        milestone = self.get_milestone(phase_key, milestone_id)
        if not milestone:
            raise KeyError(f"Milestone {milestone_id} not found in phase {phase_key}")
        if milestone.status != StatusEnum.COMPLETED and status == StatusEnum.COMPLETED:
            self.milestones_completed += 1
        milestone.status = status

    def list_milestones(self, phase_key: str) -> dict[str, Milestone]:
        """Get all milestones in a phase."""
        phase = self.get_phase(phase_key)
        if not phase:
            return {}
        return phase.milestones

    # --- Task Operations ---

    def get_task(
        self, phase_key: str, milestone_id: str, task_id: str
    ) -> Optional[Task]:
        """Get a task by phase, milestone, and task ID."""
        milestone = self.get_milestone(phase_key, milestone_id)
        if not milestone:
            return None
        return milestone.tasks.get(task_id)

    def add_task(
        self,
        phase_key: str,
        milestone_id: str,
        task_id: str,
        description: str,
        priority: bool = False,
        subagent: bool = False,
        refs: Optional[list[str]] = None,
    ) -> Task:
        """Add a task to a milestone."""
        milestone = self.get_milestone(phase_key, milestone_id)
        if not milestone:
            raise KeyError(f"Milestone {milestone_id} not found in phase {phase_key}")
        task = Task(
            description=description,
            priority=priority,
            subagent=subagent,
            refs=refs or [],
        )
        milestone.tasks[task_id] = task
        self.tasks_total += 1
        return task

    def set_task_status(
        self, phase_key: str, milestone_id: str, task_id: str, status: StatusEnum
    ) -> None:
        """Set task status."""
        task = self.get_task(phase_key, milestone_id, task_id)
        if not task:
            raise KeyError(f"Task {task_id} not found")
        if task.status != StatusEnum.COMPLETED and status == StatusEnum.COMPLETED:
            self.tasks_completed += 1
        task.status = status

    def list_tasks(self, phase_key: str, milestone_id: str) -> dict[str, Task]:
        """Get all tasks in a milestone."""
        milestone = self.get_milestone(phase_key, milestone_id)
        if not milestone:
            return {}
        return milestone.tasks

    # --- Acceptance Criteria Operations ---

    def add_acceptance_criteria(
        self,
        phase_key: str,
        milestone_id: str,
        ac_id: str,
        description: str,
    ) -> AcceptanceCriteria:
        """Add acceptance criteria to a milestone."""
        milestone = self.get_milestone(phase_key, milestone_id)
        if not milestone:
            raise KeyError(f"Milestone {milestone_id} not found in phase {phase_key}")
        ac = AcceptanceCriteria(id=ac_id, description=description)
        milestone.acceptance_criteria.append(ac)
        return ac

    def set_acceptance_criteria_met(
        self, phase_key: str, milestone_id: str, ac_id: str, met: bool
    ) -> None:
        """Set acceptance criteria met status."""
        milestone = self.get_milestone(phase_key, milestone_id)
        if not milestone:
            raise KeyError(f"Milestone {milestone_id} not found")
        for ac in milestone.acceptance_criteria:
            if ac.id == ac_id:
                ac.met = met
                return
        raise KeyError(f"Acceptance criteria {ac_id} not found")

    # --- Metadata ---

    @property
    def last_updated(self) -> datetime:
        return self._ensure_data().metadata.last_updated

    @property
    def schema_version(self) -> str:
        return self._ensure_data().metadata.schema_version

    # --- Utility ---

    def recalculate_summary(self) -> None:
        """Recalculate summary counts from actual data."""
        data = self._ensure_data()
        phases_total = 0
        phases_completed = 0
        milestones_total = 0
        milestones_completed = 0
        tasks_total = 0
        tasks_completed = 0

        for phase in data.phases.values():
            phases_total += 1
            if phase.status == StatusEnum.COMPLETED:
                phases_completed += 1
            for milestone in phase.milestones.values():
                milestones_total += 1
                if milestone.status == StatusEnum.COMPLETED:
                    milestones_completed += 1
                for task in milestone.tasks.values():
                    tasks_total += 1
                    if task.status == StatusEnum.COMPLETED:
                        tasks_completed += 1

        data.summary.phases.total = phases_total
        data.summary.phases.completed = phases_completed
        data.summary.milestones.total = milestones_total
        data.summary.milestones.completed = milestones_completed
        data.summary.tasks.total = tasks_total
        data.summary.tasks.completed = tasks_completed

    def to_dict(self) -> dict:
        """Export as dictionary."""
        return self._ensure_data().model_dump(mode="json")

    def to_json(self, indent: int = 2) -> str:
        """Export as JSON string."""
        return json.dumps(self.to_dict(), indent=indent, default=str)
