import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from utils import read_stdin_json, write_file  # type: ignore


def main() -> None:
    hook_input = read_stdin_json()
    write_file("post_tool_test.log", json.dumps(hook_input, indent=4))


if __name__ == "__main__":
    main()
