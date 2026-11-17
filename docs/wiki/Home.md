Welcome to the Trooper's Coordinator Skills wiki!

These two skills set up a two-agent workflow: **Claude coordinates, a second coding agent does the grunt work, and
the repo remembers everything.** The [README](https://github.com/Trooper-code/Trooper-s-Coordinator-Skills#readme) covers installing; this wiki covers how to use them well.

## Pages
1. [[The Workflow]]: the roles and the loop, starting a new project, and adding it to an existing one
2. [[Writing Agent Prompts]]: what makes a prompt the agent can run without you
3. [[Reviewing Agent Work]]: how Claude checks the agent's branch before merging
4. [[Session Handoffs]]: keeping context small and starting fresh chats with nothing lost
5. [[Agent Rules and Reports]]: `AGENTS.md`, agent-specific constraints, reports in the repo, stop conditions
6. [[Memory Model]]: the technical side: memory tiers, the RNN/LSTM comparison, token math
7. [[Tips and FAQ]]

## Why this works
- **Cost:** the expensive model spends its tokens on judgment (planning, reviewing), not on reading huge files
  or long traces.
- **Context:** every finding goes into committed docs, so a new chat can pick up from one small file.
- **Trust:** nothing is merged until Claude has re-run the tests and you've tested it on your own machine.
