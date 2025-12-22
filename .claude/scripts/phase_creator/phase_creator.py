#!/usr/bin/env python3
import argparse
import json
import sys
from typing import NoReturn

from operations import (
    add_acceptance_criteria,
    add_milestone,
    add_phase,
    add_task,
    get_available_subagents,
)


def error_exit(message: str) -> NoReturn:
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(1)


def success_output(data: dict) -> None:
    print(json.dumps(data, indent=2))


def cmd_phase_add(args: argparse.Namespace) -> None:
    try:
        result = add_phase(args.id, args.name)
        success_output({"status": "success", "phase": result})
    except ValueError as e:
        error_exit(str(e))


def cmd_milestone_add(args: argparse.Namespace) -> None:
    try:
        result = add_milestone(
            phase_id=args.phase,
            milestone_id=args.id,
            name=args.name,
            goal=args.goal,
            parallel=args.parallel,
            parallel_with=args.parallel_with or [],
            dependencies=args.dependencies or [],
        )
        success_output({"status": "success", "milestone": result})
    except ValueError as e:
        error_exit(str(e))


def cmd_task_add(args: argparse.Namespace) -> None:
    if args.subagent_delegation and not args.subagents:
        error_exit("--subagents is required when --subagent-delegation is set")

    try:
        result = add_task(
            phase_id=args.phase,
            milestone_id=args.milestone,
            task_id=args.id,
            description=args.description,
            priority=args.priority,
            subagent_delegation=args.subagent_delegation,
            subagents=args.subagents or [],
            dependencies=args.dependencies or [],
        )
        success_output({"status": "success", "task": result})
    except ValueError as e:
        error_exit(str(e))


def cmd_criteria_add(args: argparse.Namespace) -> None:
    try:
        result = add_acceptance_criteria(
            phase_id=args.phase,
            milestone_id=args.milestone,
            ac_id=args.id,
            description=args.description,
        )
        success_output({"status": "success", "acceptance_criteria": result})
    except ValueError as e:
        error_exit(str(e))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Manage phases, milestones, and tasks in project/status.json"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Phase command
    phase_parser = subparsers.add_parser("phase", help="Manage phases")
    phase_subparsers = phase_parser.add_subparsers(dest="action", required=True)

    phase_add = phase_subparsers.add_parser("add", help="Add a new phase")
    phase_add.add_argument("--id", required=True, help="Phase ID (e.g., '1', '2')")
    phase_add.add_argument("--name", required=True, help="Phase name")
    phase_add.set_defaults(func=cmd_phase_add)

    # Milestone command
    milestone_parser = subparsers.add_parser("milestone", help="Manage milestones")
    milestone_subparsers = milestone_parser.add_subparsers(dest="action", required=True)

    milestone_add = milestone_subparsers.add_parser("add", help="Add a new milestone")
    milestone_add.add_argument("--phase", required=True, help="Parent phase ID")
    milestone_add.add_argument("--id", required=True, help="Milestone ID (e.g., 'MS-001')")
    milestone_add.add_argument("--name", required=True, help="Milestone name")
    milestone_add.add_argument("--goal", required=True, help="Milestone goal description")
    milestone_add.add_argument("--parallel", action="store_true", help="Can run in parallel")
    milestone_add.add_argument(
        "--parallel-with", nargs="*", help="Milestone IDs to run in parallel with"
    )
    milestone_add.add_argument(
        "--dependencies", nargs="*", help="Milestone IDs this depends on"
    )
    milestone_add.set_defaults(func=cmd_milestone_add)

    # Task command
    task_parser = subparsers.add_parser("task", help="Manage tasks")
    task_subparsers = task_parser.add_subparsers(dest="action", required=True)

    task_add = task_subparsers.add_parser("add", help="Add a new task")
    task_add.add_argument("--phase", required=True, help="Parent phase ID")
    task_add.add_argument("--milestone", required=True, help="Parent milestone ID")
    task_add.add_argument("--id", required=True, help="Task ID (e.g., 'T001')")
    task_add.add_argument("--description", required=True, help="Task description")
    task_add.add_argument("--priority", action="store_true", help="Mark as priority/critical path")
    task_add.add_argument(
        "--subagent-delegation", action="store_true", help="Enable subagent delegation"
    )
    available_agents = get_available_subagents()
    task_add.add_argument(
        "--subagents",
        nargs="*",
        choices=available_agents if available_agents else None,
        help=f"Subagents to use. Available: {available_agents}",
    )
    task_add.add_argument("--dependencies", nargs="*", help="Task IDs this depends on")
    task_add.set_defaults(func=cmd_task_add)

    # Criteria command
    criteria_parser = subparsers.add_parser("criteria", help="Manage acceptance criteria")
    criteria_subparsers = criteria_parser.add_subparsers(dest="action", required=True)

    criteria_add = criteria_subparsers.add_parser("add", help="Add acceptance criteria")
    criteria_add.add_argument("--phase", required=True, help="Parent phase ID")
    criteria_add.add_argument("--milestone", required=True, help="Parent milestone ID")
    criteria_add.add_argument("--id", required=True, help="Criteria ID (e.g., 'AC-001')")
    criteria_add.add_argument("--description", required=True, help="Criteria description")
    criteria_add.set_defaults(func=cmd_criteria_add)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
