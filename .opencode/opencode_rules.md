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