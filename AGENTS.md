# AGENTS.md - IS 4010 Final Project

## April 28, 2026
- **Task**: Initial repository setup and environment configuration.
- **AI Tool**: Gemini / VS Code AI.
- **Collaboration**: AI helped troubleshoot terminal directory errors (finding the correct repo folder) and guided the creation of the Python virtual environment.

## April 28, 2026
- **Task**: Built CLI tool, tests, and CI workflow.
- **AI Tool**: GitHub Copilot / VS Code AI.
- **Collaboration**: AI generated the first `main.py` CLI skeleton, helped add error handling for API failures, and created a GitHub Actions workflow. I verified the code, fixed dependency installation, and confirmed `pytest` passes.
- **What I learned**: AI can create a working structure quickly, but I had to review and improve the error handling, ensure the API token is loaded from `.env`, and add realistic README usage examples.
- **What I fixed**: I rewrote the README to include a project description, installation steps, command examples, expected output, and future improvement notes. I also added a `.env.example`, a proper `main()` entry point, and a tests file covering core functionality.

## April 28, 2026
- **Task**: Maximize rubric score with edge-case tests and CLI validation.
- **AI Tool**: GitHub Copilot / VS Code AI.
- **Collaboration**: AI suggested additional validation and edge-case handling. I expanded the test suite to include network failures, invalid top flags, and malformed API responses, and I improved README setup details.

## April 28, 2026
- **Task**: Added matches fetching feature.
- **AI Tool**: GitHub Copilot / VS Code AI.
- **Collaboration**: AI helped add a new `--matches` flag and `fetch_matches` function to extend the CLI beyond standings.
- **What I learned**: Extending CLI tools with new features requires careful integration of API calls and output formatting.

## April 28, 2026
- **Task**: Added top scorers feature.
- **AI Tool**: GitHub Copilot / VS Code AI.
- **Collaboration**: AI helped add `--scorers` flag and `fetch_scorers` function for player statistics.
- **What I learned**: Adding multiple data sources enhances the tool's utility while maintaining clean code structure.
