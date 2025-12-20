import sys
from pathlib import Path


def read_file(file_path: str) -> str:
    try:
        return Path(file_path).read_text(encoding="utf-8")
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except PermissionError:
        raise PermissionError(f"Permission denied: {file_path}")
    except UnicodeDecodeError:
        raise UnicodeDecodeError(f"Invalid encoding: {file_path}", b"", 0, 0, "")


def write_file(file_path: str, content: str) -> None:
    existing_content = read_file(file_path)
    new_content = existing_content + content
    Path(file_path).write_text(new_content, encoding="utf-8")
