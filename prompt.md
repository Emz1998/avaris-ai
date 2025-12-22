Create a status logger hook that will change the task status of the roadmap in '/home/emhar/avaris-ai/project/{version}/release-plan/release-plan.md'.

- Use the "PreToolUse" HookEvent with "Skill" Matcher.
- The Skill Input has changed .Please check'/home/emhar/avaris-ai/pre_tool_test.log'. Now you must parse the the tool_input.skill and .args.

## Instructions

- Parse the tool_input.skill and .args.
- If "skill" is not log:task, then exit(0).
- Validate the .args. If the .args is not a valid task id, then block the tool execution with Exit(2)
- Retrieve the current task in @project/{version}/release-plan/roadmap.json
- To get the version, retrieve it from the @project/product.json file.

The valid .args input is this : "<task-id> <status>"
Valid statuses are: completed, in_progress, blocked
Example: "T001 completed"

Also you must validate if task-id exist in the roadmap.json and valid format (TNNN)
