from typing import Any, Self


class DotAccessor:
    """Wrapper that enables dot notation access to nested dicts."""

    def __init__(self, data: dict[str, Any] | None):
        self._data = data or {}

    def __getattr__(self, name: str) -> Any:
        if name.startswith("_"):
            return super().__getattribute__(name)
        value = self._data.get(name)
        if isinstance(value, dict):
            return DotAccessor(value)
        return value

    def __repr__(self) -> str:
        return repr(self._data)

    def to_dict(self) -> dict[str, Any]:
        return self._data


class QueryBuilder:
    """Fluent builder for querying project roadmap data."""

    def __init__(self, data: dict[str, Any]):
        self._data = data
        self._phase_id: int | None = None
        self._milestone_id: int | None = None
        self._task_id: int | None = None

    def phase(self, phase_id: int) -> Self:
        self._phase_id = phase_id
        return self

    def milestone(self, milestone_id: int) -> Self:
        self._milestone_id = milestone_id
        return self

    def task(self, task_id: int) -> Self:
        self._task_id = task_id
        return self

    def _build_path(self) -> list[str]:
        path = []
        if self._phase_id is not None:
            path.extend(["phases", str(self._phase_id)])
        if self._milestone_id is not None:
            path.extend(["milestones", f"MS-{self._milestone_id:03d}"])
        if self._task_id is not None:
            path.extend(["tasks", f"T{self._task_id:03d}"])
        return path

    def _resolve(self) -> dict[str, Any] | None:
        result = self._data
        for key in self._build_path():
            if isinstance(result, dict) and key in result:
                result = result[key]
            else:
                return None
        return result

    def get(self) -> DotAccessor:
        return DotAccessor(self._resolve())


class Project:
    def __init__(self, status_data: dict[str, Any]):
        self._status_data = status_data

    @property
    def status_data(self) -> dict[str, Any]:
        return self._status_data

    @status_data.setter
    def status_data(self, value: dict[str, Any]) -> None:
        self._status_data = value

    @property
    def query(self) -> QueryBuilder:
        return QueryBuilder(self._status_data)

    @property
    def info(self) -> DotAccessor:
        return DotAccessor(self._status_data.get("project"))

    @property
    def specs(self) -> DotAccessor:
        return DotAccessor(self._status_data.get("specs"))

    @property
    def summary(self) -> DotAccessor:
        return DotAccessor(self._status_data.get("summary"))

    @property
    def current(self) -> DotAccessor:
        return DotAccessor(self._status_data.get("current"))


if __name__ == "__main__":
    sample_data = {
        "project": {
            "name": "NEXLY RN",
            "version": "0.1.0",
            "target_release": "2026-01-01",
            "status": "in_progress",
        },
        "specs": {
            "prd": {"status": "completed", "path": "specs/prd.md"},
            "tech": {"status": "in_progress", "path": "specs/tech.md"},
            "ux": {"status": "not_started", "path": "specs/ux.md"},
        },
        "summary": {
            "phases": {"total": 3, "completed": 0},
            "milestones": {"total": 10, "completed": 1},
            "tasks": {"total": 50, "completed": 5},
        },
        "current": {"phase": "1", "milestone": "MS-001", "task": "T002"},
        "phases": {
            "1": {
                "name": "Foundation",
                "status": "in_progress",
                "milestones": {
                    "MS-001": {
                        "name": "Environment Setup",
                        "status": "completed",
                        "tasks": {
                            "T001": {
                                "description": "Initialize project",
                                "status": "completed",
                            },
                            "T002": {
                                "description": "Configure tooling",
                                "status": "in_progress",
                            },
                        },
                    }
                },
            }
        },
    }

    project = Project(sample_data)

    # Fluent access for info
    print("=== Project Info ===")
    print(f"project.info.name: {project.info.name}")
    print(f"project.info.version: {project.info.version}")
    print(f"project.info.status: {project.info.status}")

    # Fluent access for specs
    print("\n=== Specs ===")
    print(f"project.specs.prd.status: {project.specs.prd.status}")
    print(f"project.specs.prd.path: {project.specs.prd.path}")
    print(f"project.specs.tech.status: {project.specs.tech.status}")
    print(f"project.specs.ux.status: {project.specs.ux.status}")

    # Fluent access for summary
    print("\n=== Summary ===")
    print(f"project.summary.phases.total: {project.summary.phases.total}")
    print(f"project.summary.phases.completed: {project.summary.phases.completed}")
    print(f"project.summary.milestones.total: {project.summary.milestones.total}")
    print(f"project.summary.tasks.completed: {project.summary.tasks.completed}")

    # Fluent access for current
    print("\n=== Current ===")
    print(f"project.current.phase: {project.current.phase}")
    print(f"project.current.milestone: {project.current.milestone}")
    print(f"project.current.task: {project.current.task}")

    # Method chaining for roadmap query
    print("\n=== Query: Phase 1 > Milestone 1 > Task 1 ===")
    task = project.query.phase(1).milestone(1).task(1).get()
    print(f"task.description: {task.description}")
    print(f"task.status: {task.status}")

    print("\n=== Query: Phase 1 > Milestone 1 ===")
    milestone = project.query.phase(1).milestone(1).get()
    print(f"milestone.name: {milestone.name}")
    print(f"milestone.status: {milestone.status}")
