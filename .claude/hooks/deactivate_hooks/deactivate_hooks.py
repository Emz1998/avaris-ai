import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import read_stdin_json  # type: ignore


def main() -> None:
    hook_input = read_stdin_json()
    print(hook_input)
    sys.exit(0)


if __name__ == "__main__":
    main()
