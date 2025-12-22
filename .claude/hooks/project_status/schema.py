"""
Pydantic schema model for project/status.json.
Single source of truth for project progress tracking.
"""
from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class StatusEnum(str, Enum):
    """Status values for project, phases, milestones, and tasks."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"


class SpecStatusEnum(str, Enum):
    """Status values for specification documents."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Project(BaseModel):
    """Project-level metadata."""
    name: str = Field(..., description="Project display name")
    version: str = Field(..., description="Current version (semver)")
    target_release: str = Field(..., description="Target release date (ISO 8601)")
    status: StatusEnum = Field(default=StatusEnum.NOT_STARTED)


class SpecItem(BaseModel):
    """Individual specification document status."""
    status: SpecStatusEnum = Field(default=SpecStatusEnum.NOT_STARTED)
    path: str = Field(..., description="Relative path to spec file")


class Specs(BaseModel):
    """Specification documents tracking."""
    prd: SpecItem = Field(default_factory=lambda: SpecItem(path="specs/prd.md"))
    tech: SpecItem = Field(default_factory=lambda: SpecItem(path="specs/tech.md"))
    ux: SpecItem = Field(default_factory=lambda: SpecItem(path="specs/ux.md"))


class CountSummary(BaseModel):
    """Aggregate count for a category."""
    total: int = Field(default=0, ge=0)
    completed: int = Field(default=0, ge=0)


class Summary(BaseModel):
    """Aggregate counts for quick status overview."""
    phases: CountSummary = Field(default_factory=CountSummary)
    milestones: CountSummary = Field(default_factory=CountSummary)
    tasks: CountSummary = Field(default_factory=CountSummary)


class Current(BaseModel):
    """Tracks currently active work."""
    phase: Optional[str] = Field(default=None, description="Current phase number")
    milestone: Optional[str] = Field(default=None, description="Current milestone ID")
    task: Optional[str] = Field(default=None, description="Current task ID")


class Task(BaseModel):
    """Individual task within a milestone."""
    description: str = Field(..., description="What the task accomplishes")
    priority: bool = Field(default=False, description="True if [P] - critical path")
    subagent_delegation: bool = Field(default=False, description="True if delegatable to subagent")
    subagents: list[str] = Field(default_factory=list, description="Subagent types for delegation")
    dependencies: list[str] = Field(default_factory=list, description="Task dependencies")
    acceptance_criteria: list[str] = Field(default_factory=list, description="Task-level AC")
    status: StatusEnum = Field(default=StatusEnum.NOT_STARTED)


class AcceptanceCriteria(BaseModel):
    """Acceptance criteria for milestone completion."""
    id: str = Field(..., pattern=r"^AC-\d{3}$", description="Unique ID (AC-###)")
    description: str = Field(..., description="What must be true for acceptance")
    met: bool = Field(default=False, description="Whether criteria is satisfied")


class Milestone(BaseModel):
    """Milestone containing tasks and acceptance criteria."""
    name: str = Field(..., description="Milestone name")
    goal: str = Field(..., description="What this milestone achieves")
    parallel: bool = Field(default=False, description="Can run in parallel")
    parallel_with: list[str] = Field(default_factory=list, description="Parallel IDs")
    dependencies: list[str] = Field(default_factory=list, description="Required IDs")
    status: StatusEnum = Field(default=StatusEnum.NOT_STARTED)
    tasks: dict[str, Task] = Field(default_factory=dict, description="Task ID -> Task")
    acceptance_criteria: list[AcceptanceCriteria] = Field(default_factory=list)
    verification: list[str] = Field(default_factory=list, description="Verification steps")


class Phase(BaseModel):
    """Project phase containing milestones."""
    id: str = Field(..., pattern=r"^phase-\d+$", description="Unique phase ID")
    name: str = Field(..., description="Phase name/description")
    status: StatusEnum = Field(default=StatusEnum.NOT_STARTED)
    milestones: dict[str, Milestone] = Field(
        default_factory=dict,
        description="Milestone ID (MS-###) -> Milestone"
    )


class Metadata(BaseModel):
    """Schema metadata."""
    last_updated: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    schema_version: str = Field(default="1.0.0")


class ProjectStatus(BaseModel):
    """
    Root schema for project/status.json.
    Single source of truth for project progress tracking.
    """
    project: Project
    specs: Specs = Field(default_factory=Specs)
    summary: Summary = Field(default_factory=Summary)
    current: Current = Field(default_factory=Current)
    phases: dict[str, Phase] = Field(
        default_factory=dict,
        description="Phase number (string) -> Phase"
    )
    metadata: Metadata = Field(default_factory=Metadata)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() + "Z"
        }
