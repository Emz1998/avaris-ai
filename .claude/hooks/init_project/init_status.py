#

import sys
from pathlib import Path
from typing import Any
from pydantic import BaseModel

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import set_status  # type: ignore


class Status(BaseModel):
    version: str
    project_name: str
    project_status: bool
    current_phase_num: int
    current_phase: str
    current_phase_status: bool
    current_milestone: str
    current_milestone_status: bool
    total_phases: int
    phases_completed: int
    phases_remaining: int
    total_milestones: int
    milestones_completed: int
    milestones_remaining: int
    total_tasks: int
    tasks_completed: int
    tasks_remaining: int


def init_status(status: Status) -> bool:
    for key, value in status.model_dump().items():
        set_status(key, value)
    return True
