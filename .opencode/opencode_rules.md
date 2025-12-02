# OpenCode Rules for AI Agents

## Session Start Workflow

Each time a new development session begins:

1. Check if the local git repository is clean (no uncommitted changes).
2. **Only if the repository is clean**:
   - Check for remote changes and pull them (including all branches to ensure sync across multiple machines).
   - Ask the developer if the work is for a new feature or bugfix.
3. Create an appropriate branch:
   - `feature/branch-name` for new features
   - `bugfix/branch-name` for bug fixes
4. Follow standard git processes for commits and pushes to the branch.
5. When work is complete, create a pull request and merge back to `master` (or `main`).
6. Explain all git operations performed during the session.

This ensures organized development, proper branching, clear communication of changes, and synchronization across multiple development machines.

## Script Management Workflow

- A `new_scripts/` directory has been created for user-placed scripts (Python, PowerShell, etc.).
- This directory serves as a 'new feature' staging area.
- Scripts placed here are not to be packaged or included in the TUI until explicitly requested for implementation.
- When the user requests implementation of a script into the TUI:
  1. Move the script from `new_scripts/` to `scripts/`.
  2. Integrate it into the TUI functionality.
  3. Follow the standard git workflow for the implementation.
- This keeps the codebase clean and ensures scripts are only included when properly integrated.