from typing import Any, Self
from flatten_dict import flatten, unflatten


class DotAccessor:
    """Enables dot notation access using flattened dict lookup."""

    def __init__(self, flat_data: dict[str, Any], prefix: str = ""):
        self._flat = flat_data
        self._prefix = prefix

    def __getattr__(self, name: str) -> Any:
        if name.startswith("_"):
            return super().__getattribute__(name)
        path = f"{self._prefix}.{name}" if self._prefix else name
        # Check if it's a leaf value
        if path in self._flat:
            return self._flat[path]
        # Check if it's a nested path (has children)
        if any(k.startswith(f"{path}.") for k in self._flat):
            return DotAccessor(self._flat, path)
        return None

    def __repr__(self) -> str:
        return f"DotAccessor(prefix='{self._prefix}')"


class QueryBuilder:
    """Fluent builder for querying roadmap with phase/milestone/task IDs."""

    def __init__(self, flat_data: dict[str, Any]):
        self._flat = flat_data
        self._path_parts: list[str] = []

    def phase(self, phase_id: int) -> Self:
        self._path_parts.extend(["phases", str(phase_id)])
        return self

    def milestone(self, milestone_id: int) -> Self:
        self._path_parts.extend(["milestones", f"MS-{milestone_id:03d}"])
        return self

    def task(self, task_id: int) -> Self:
        self._path_parts.extend(["tasks", f"T{task_id:03d}"])
        return self

    def get(self, field: str | None = None) -> Any:
        path = ".".join(self._path_parts)
        if field:
            path = f"{path}.{field}"
        return self._flat.get(path)

    def status(self) -> str | None:
        return self.get("status")


class Project:
    def __init__(self, status_data: dict[str, Any]):
        self._data = status_data
        self._flat = flatten(status_data, reducer="dot")

    def get(self, path: str) -> Any:
        return self._flat.get(path)

    def set(self, path: str, value: Any) -> None:
        self._flat[path] = value
        self._data = unflatten(self._flat, splitter="dot")

    @property
    def data(self) -> dict[str, Any]:
        return self._data

    @property
    def query(self) -> QueryBuilder:
        return QueryBuilder(self._flat)

    @property
    def info(self) -> DotAccessor:
        return DotAccessor(self._flat, "project")

    @property
    def specs(self) -> DotAccessor:
        return DotAccessor(self._flat, "specs")

    @property
    def summary(self) -> DotAccessor:
        return DotAccessor(self._flat, "summary")

    @property
    def current(self) -> DotAccessor:
        return DotAccessor(self._flat, "current")


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

    # Fluent dot notation access
    print("=== Project Info ===")
    print(f"project.info.name: {project.info.name}")
    print(f"project.info.version: {project.info.version}")
    print(f"project.info.status: {project.info.status}")

    print("\n=== Specs ===")
    print(f"project.specs.prd.status: {project.specs.prd.status}")
    print(f"project.specs.prd.path: {project.specs.prd.path}")
    print(f"project.specs.tech.status: {project.specs.tech.status}")

    print("\n=== Summary ===")
    print(f"project.summary.phases.total: {project.summary.phases.total}")
    print(f"project.summary.milestones.completed: {project.summary.milestones.completed}")

    print("\n=== Current ===")
    print(f"project.current.phase: {project.current.phase}")
    print(f"project.current.milestone: {project.current.milestone}")
    print(f"project.current.task: {project.current.task}")

    # String path access (also works)
    print("\n=== String Path Access ===")
    print(f"project.get('specs.prd.status'): {project.get('specs.prd.status')}")

    # Method chaining for roadmap query
    print("\n=== Query Builder ===")
    print(f"project.query.phase(1).milestone(1).task(1).status(): {project.query.phase(1).milestone(1).task(1).status()}")
    print(f"project.query.phase(1).milestone(1).get('name'): {project.query.phase(1).milestone(1).get('name')}")
