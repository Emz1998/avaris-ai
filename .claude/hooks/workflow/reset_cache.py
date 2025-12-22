import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import set_cache  # type: ignore


def reset_cache() -> None:
    """Reset the cache."""
    set_cache(
        "block_stoppage", {"condition": False, "reason": "Phase transition allowed"}
    )
    set_cache("phases_completed", [])
    set_cache("skills_triggered", [])
    set_cache("subagents_triggered", [])
    set_cache("active_subagent", "")
    set_cache("current_phase", "explore")
