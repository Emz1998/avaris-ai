import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent))

from utils import get_status, set_status  # type: ignore
from init_status import init_status, Status  # type: ignore


STATUS_FILE = Path(__file__).parent.parent.parent.parent / "project" / "status.json"

SPEC_DIR = [
    "brainstorm-summary.md",
    "prd.md",
    "tech-specs.md",
    "ux.md",
]


RELEASE_PLAN_DIR = [
    "roadmap.json",
    "roadmap.md",
    "overview.md",
]

MILESTONE_DIR = [
    "decisions",
    "plans",
    "research",
    "codebase-status",
    "revisions",
    "reports",
    "misc",
    "status.json",
]


def build_project_dir(version: str, milestone_name: str) -> dict[str, Any]:
    project_dir: dict[str, Any] = {
        "project": [
            {
                version: {
                    "specs": SPEC_DIR,
                    "release-plan": RELEASE_PLAN_DIR,
                    "milestones": {
                        milestone_name: MILESTONE_DIR,
                    },
                }
            },
            "status.json",
        ],
    }
    return project_dir


project_status = Status(
    version="v0.1.0",
    project_name="Avaris - NBA Betting Analytics Application",
    project_status=False,
    current_phase_num=0,
    current_phase="",
    current_phase_status=False,
    current_milestone="",
    current_milestone_status=False,
    total_phases=0,
    phases_completed=0,
    phases_remaining=0,
    total_milestones=0,
    milestones_completed=0,
    milestones_remaining=0,
    total_tasks=0,
    tasks_completed=0,
    tasks_remaining=0,
)


def init_dir(dir_path: str) -> Path:
    path = Path(dir_path)
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
    return path


def init_file(file_path: str) -> Path:
    path = Path(file_path)
    if not path.exists():
        path.touch()
    return path


def init_project(item: Any, project_path: str) -> str:
    if type(item) == str:
        if item.endswith((".json", ".md")):
            init_file(f"{project_path}{item}")
        else:
            init_dir(f"{project_path}{item}")
    elif type(item) == dict:
        for key, value in item.items():
            init_dir(f"{project_path}{key}")
            init_project(value, f"{project_path}{key}/")
    elif type(item) == list:
        for item in item:
            init_project(item, project_path)
    else:
        raise ValueError(f"Invalid item type: {type(item)}")
    return project_path


def main() -> bool:
    init_dir("project")
    init_status(project_status)
    current_milestone = get_status("current_milestone")
    current_version = get_status("version")
    project_dir = build_project_dir(
        version=current_version, milestone_name=current_milestone
    )
    init_project(project_dir, "")
    return True


if __name__ == "__main__":
    main()
