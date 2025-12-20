from typing import Any
from pathlib import Path
import json
from typing import Optional

from .json_handler import load_json


def set_cache(key: str, value: Any, file_path: str = "") -> None:
    data = load_json(file_path)
    data[key] = value
    Path(file_path).write_text(json.dumps(data, indent=2))


def get_cache(key: str, default: Optional[Any] = None, file_path: str = "") -> Any:
    data = load_json(file_path)
    return data.get(key, default)


def clear_cache(file_path: str) -> None:
    set_cache("hooks", {}, file_path)
