#!/usr/bin/env python3
"""Block stoppage if the current milestone is not completed."""

import json
import sys
from pathlib import Path
from typing import NoReturn

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import read_stdin_json  # type: ignore
from utils.roadmap import (  # type: ignore[import-not-found]
    find_milestone_in_roadmap,
    get_current_version,
    get_roadmap_path,
    load_roadmap,
)


def block_stoppage(reason: str) -> NoReturn:
    """Output JSON to block stoppage and exit 0."""
    output = {
        "decision": "block",
        "reason": reason,
    }
    print(json.dumps(output))
    sys.exit(0)


def allow_stoppage() -> NoReturn:
    """Output JSON to allow stoppage with continue: true."""
    output = {"continue": True}
    print(json.dumps(output))
    sys.exit(0)


def main() -> None:
    """Main stop guard logic."""
    try:
        read_stdin_json()

        # Get current version and roadmap
        version = get_current_version()
        if not version:
            allow_stoppage()

        roadmap_path = get_roadmap_path(version)
        if not roadmap_path.exists():
            allow_stoppage()

        roadmap = load_roadmap(roadmap_path)
        if roadmap is None:
            allow_stoppage()

        # Get current milestone from roadmap
        current = roadmap.get("current", {})
        current_milestone_id = current.get("milestone")

        if not current_milestone_id:
            allow_stoppage()

        # Find the current milestone
        _, milestone = find_milestone_in_roadmap(roadmap, current_milestone_id)
        if milestone is None:
            allow_stoppage()

        # Check if current milestone is completed
        milestone_status = milestone.get("status", "pending")
        if milestone_status != "completed":
            reason = (
                f"Cannot stop. Current milestone '{current_milestone_id}' "
                f"is '{milestone_status}'. Complete the milestone before stopping."
            )
            block_stoppage(reason)

        # Current milestone is completed, allow stoppage
        allow_stoppage()

    except Exception as e:
        # On error, log and allow stoppage to avoid blocking indefinitely
        print(f"Stop guard error: {e}", file=sys.stderr)
        allow_stoppage()


if __name__ == "__main__":
    main()
