- Read the python files in @.claude/hooks/status_logger
- Create a seperate acceptance criteria logger that will be used to change the status of the acceptance criteria in @project/{version}/release-plan/roadmap.md

- Also create a success criteria logger that will be used to change the status of the success criteria in @project/{version}/release-plan/roadmap.md
- If acceptance criteria or success criteria is met, change the status of acceptance_critria.met or success_criteria.met to "true", otherwise keep it as "false"

- Same thing as task logger you have to verify the Skill Args.
- The skill name that needed to be detected is: /log:ac or /log:sc
- The valid Args are: <AC-NNN> <status>
- Example: /log:ac AC-001 true or /log:sc SC-001 false
- Please read the roadmap first to understand the structure of the roadmap
- To get the version, read @project/product.json
