Create a discussion slash command that helps the user discuss the implementation strategy for a project and make decisions for the current task. Must use the `AskUserQuestion` tool for interactive questions and collaboration.

All your output should use the `AskUserQuestion` tool to get the user's feedback and discuss the best way to implement the current task. A discussion session is completed once the user says it's done. You can check if we are done by also using the `AskUserQuestion` tool to ask if we are done or if we need to discuss more ideas. Once done, you should create a `project/v0.1.0/milestones/[MS-NNN]_[Milestone-Description]/decisions/decision_[date]_[session-id].md` file with all the decisions made during the discussion session.

Rules:

- Avoid using any other tools or output styles aside from `AskUserQuestion`.
- If deemed done, use the `AskUserQuestion` tool to ask if we are done or if we need to discuss more strategies.
- If the user says it's done, use the `AskUserQuestion` tool to ask if we can start creating the `project/v0.1.0/milestones/[MS-NNN]_[Milestone-Description]/decisions/decision_[date]_[session-id].md` file with all the decisions made during the discussion session.
