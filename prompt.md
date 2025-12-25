Revise @.claude/hooks/workflow/subagent_order_validation.py

Instead of validating by order, validate by the subagent by current phase. If the phase is explore, only codebase-explorer is allowed to be triggered. If the phase is plan, only planner is allowed to be triggered. If the phase is plan:consult, only plan-consultant is allowed to be triggered. If the phase is code, only test-engineer, fullstack-developer, code-reviewer is allowed to be triggered (this phase should be the only one in order) . If the phase is commit, only version-manager is allowed to be triggered.
