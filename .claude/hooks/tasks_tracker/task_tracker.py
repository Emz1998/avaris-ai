import sys
import json
from pathlib import Path
from flatten_json import flatten

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import read_stdin_json, load_json, set_json, get_json  # type: ignore

CACHE_PATH = Path(".claude/hooks/tasks_tracker/cache.json")


def set_tasks_status(status: str) -> None:
    for task in tasks:
        task["status"] = status
    set_json("tasks", tasks, str(CACHE_PATH))


def main() -> None:

    response = {
        "updatedInput": [
            {
                "content": "Do Spotify Frontend",
            },
            {
                "content": "Do Spotify Backend",
            },
        ],
    }
    print(json.dumps(response))
    sys.exit(0)


if __name__ == "__main__":
    main()
