#!/usr/bin/env python3
# Success Criteria Status Logger Module

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.output import log, block_response
from utils.validation import validate_sc, InvalidFormatError
from utils.roadmap import (
    get_current_version,
    get_roadmap_path,
    load_roadmap,
    save_roadmap,
    find_sc_in_roadmap,
)

VALID_STATUSES = ["met", "unmet"]


def parse_args(args_str: str) -> tuple[str, str] | None:
    """Parse args string in format '<sc-id> <status>'."""
    if not args_str:
        return None
    parts = args_str.strip().split()
    if len(parts) != 2:
        return None
    return parts[0], parts[1]


def validate_status(status: str) -> bool:
    """Validate status is one of the valid statuses."""
    return status in VALID_STATUSES


def process(args: str) -> None:
    """Process success criteria status update."""
    parsed = parse_args(args)
    if parsed is None:
        block_response(
            "Invalid args format. Expected: '<SC-NNN> <status>'. Example: 'SC-001 met'"
        )

    sc_id, status = parsed

    try:
        validate_sc(sc_id)
    except InvalidFormatError as e:
        block_response(str(e))

    if not validate_status(status):
        block_response(
            f"Invalid status: '{status}'. Valid statuses: {', '.join(VALID_STATUSES)}"
        )

    version = get_current_version()
    if not version:
        block_response("Could not retrieve current_version from project/product.json")

    roadmap_path = get_roadmap_path(version)
    if not roadmap_path.exists():
        block_response(f"Roadmap not found at: {roadmap_path}")

    roadmap = load_roadmap(roadmap_path)
    if roadmap is None:
        block_response(f"Could not load roadmap from: {roadmap_path}")

    milestone, sc = find_sc_in_roadmap(roadmap, sc_id)
    if sc is None:
        block_response(f"Success criteria '{sc_id}' not found in roadmap")

    sc["status"] = status
    if not save_roadmap(roadmap_path, roadmap):
        block_response(f"Failed to update success criteria status for '{sc_id}'")

    log(f"Success criteria '{sc_id}' status updated to '{status}'")
    sys.exit(0)
