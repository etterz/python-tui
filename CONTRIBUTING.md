# Contributing to Python TUI Script Runner

Thank you for your interest in contributing to the Python TUI Script Runner! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Reporting Issues](#reporting-issues)

## Code of Conduct

This project follows a code of conduct to ensure a welcoming environment for all contributors. By participating, you agree to:

- Be respectful and inclusive
- Focus on constructive feedback
- Accept responsibility for mistakes
- Show empathy towards other contributors
- Help create a positive community

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Git
- Familiarity with TUI development and Textual framework

### Development Setup

1. Fork the repository on GitHub
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/python-tui.git
   cd python-tui
   ```

3. Set up the development environment:
   ```bash
   python init.py
   ```

4. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

5. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

## Development Workflow

### Session Start Workflow

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

### Branching Strategy

- `main`: Production-ready code
- `develop`: Integration branch for features
- `feature/*`: New features
- `bugfix/*`: Bug fixes
- `hotfix/*`: Critical fixes for production

### Making Changes

1. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes following the coding standards

3. Write tests for new functionality

4. Run the test suite:
   ```bash
   pytest tests/ -v
   ```

5. Format and lint your code:
   ```bash
   black tui/ tests/
   isort tui/ tests/
   pylint tui/ tests/
   mypy tui/ --strict
   ```

6. Update documentation if needed

## Coding Standards

### Python Style

- Follow PEP 8 style guidelines
- Use type hints for all function parameters and return values
- Write docstrings for all public functions, classes, and modules
- Keep line length under 88 characters (Black default)

### Code Structure

- Organize imports: standard library, third-party, local
- Use meaningful variable and function names
- Keep functions small and focused on single responsibility
- Use classes for complex state management

### TUI Development

- Use Textual's reactive model for state changes
- Implement proper error handling in UI components
- Ensure keyboard accessibility
- Test UI components with Textual's testing framework

### Commit Messages

Follow conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New features
- `fix`: Bug fixes
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test additions/modifications
- `chore`: Maintenance tasks

Examples:
```
feat(ui): add script filtering by type
fix(execution): handle timeout errors gracefully
docs(readme): update installation instructions
```

## Testing

### Test Structure

- **Unit Tests** (`tests/unit/`): Test individual functions and classes
- **Integration Tests** (`tests/integration/`): Test component interactions
- **UI Tests** (`tests/ui/`): Test Textual interface behavior

### Writing Tests

- Use descriptive test names
- Test both success and failure cases
- Mock external dependencies
- Aim for high test coverage (>90%)

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=tui --cov-report=html

# Run specific test file
pytest tests/unit/test_script_executor.py

# Run tests matching pattern
pytest -k "test_execute"
```

## Submitting Changes

### Pull Request Process

1. Ensure your branch is up-to-date with `develop`:
   ```bash
   git checkout develop
   git pull origin develop
   git checkout your-feature-branch
   git rebase develop
   ```

2. Push your branch to GitHub:
   ```bash
   git push origin your-feature-branch
   ```

3. Create a Pull Request on GitHub:
   - Use a clear, descriptive title
   - Provide detailed description of changes
   - Reference any related issues
   - Request review from maintainers

4. Address review feedback:
   - Make requested changes
   - Update tests if needed
   - Rebase and force-push if necessary

### Pull Request Requirements

- [ ] Tests pass locally
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Commit messages follow conventions
- [ ] No merge conflicts
- [ ] Reviewed by at least one maintainer

## Reporting Issues

### Bug Reports

When reporting bugs, please include:

- **Description**: Clear description of the issue
- **Steps to Reproduce**: Step-by-step instructions
- **Expected Behavior**: What should happen
- **Actual Behavior**: What actually happens
- **Environment**: Python version, OS, dependencies
- **Logs/Error Messages**: Any relevant output

### Feature Requests

For new features, please provide:

- **Description**: What feature you want
- **Use Case**: Why you need this feature
- **Proposed Solution**: How you think it should work
- **Alternatives**: Other approaches considered

### Security Issues

For security vulnerabilities:

- **DO NOT** create public issues
- Email security@project-domain.com (if available)
- Or use GitHub's security advisory feature

## Recognition

Contributors will be recognized in:
- CHANGELOG.md for significant changes
- GitHub contributors list
- Release notes

Thank you for contributing to make this project better!</content>
<parameter name="filePath">CONTRIBUTING.md