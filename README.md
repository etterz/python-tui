# Python TUI Script Runner

A secure, terminal user interface (TUI) application for discovering, managing, and executing custom scripts with comprehensive safety controls and real-time output streaming.

## Features

- **Script Discovery**: Automatically finds and categorizes executable scripts (Python, Shell)
- **Safe Execution**: Path validation, timeout protection, and command injection prevention
- **Real-time Output**: Stream script output directly to the TUI interface
- **Keyboard Navigation**: Full keyboard-driven interface with intuitive shortcuts
- **Security-First**: Built-in security scanning and vulnerability checks
- **Comprehensive Testing**: Unit, integration, and UI tests with coverage reporting
- **Code Quality**: Automated formatting, linting, and type checking

## Installation

### Prerequisites

- Python 3.9 or higher
- Git (for cloning the repository)

### Quick Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd python-tui
   ```

2. **Initialize the project**:
   ```bash
   python init.py
   ```
   This automated setup will:
   - Check Python version compatibility
   - Create a virtual environment (`venv/`)
   - Install all dependencies
   - Set up project directory structure
   - Create configuration files

3. **Activate the virtual environment**:
   - **Windows**: `venv\Scripts\activate`
   - **Linux/Mac**: `source venv/bin/activate`

## Usage

### Running the Application

Start the TUI:
```bash
python main.py
```

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Tab` | Navigate between panels |
| `↑/↓` | Navigate script list |
| `Enter` | Select/execute script |
| `Ctrl+C` | Exit application |
| `F1` | Show help |
| `Ctrl+R` | Refresh script list |
| `Ctrl+F` | Filter scripts |

### Script Management

Scripts should be placed in the `scripts/` directory. The application supports:
- Python scripts (`.py`)
- Shell scripts (`.sh`, executable permissions required)
- Script metadata via `scripts/config.json`

Example `scripts/config.json`:
```json
{
  "sample.py": {
    "description": "Sample Python script",
    "category": "examples",
    "timeout": 30
  }
}
```

## Development

### Testing

Run the complete test suite:
```bash
pytest tests/ -v
```

Run tests with coverage reporting:
```bash
pytest tests/ --cov=tui --cov-report=term-missing --cov-report=html
```

### Code Quality Tools

**Formatting**:
```bash
black tui/ tests/
isort tui/ tests/
```

**Linting & Type Checking**:
```bash
pylint tui/ tests/
mypy tui/ --strict
```

**Security Scanning**:
```bash
bandit -r tui/ -ll
safety check --json
```

### VS Code Integration

The project includes VS Code configuration files (`.vscode/tasks.json` and `.vscode/launch.json`) for:
- Running tests and coverage
- Debugging the TUI application
- Code formatting and linting
- Security scanning

Use `Ctrl+Shift+P` → "Tasks: Run Task" to access development tasks.

## Project Structure

```
python-tui/
├── main.py                    # Application entry point
├── init.py                    # Project initialization script
├── tui/                       # TUI application modules
│   ├── app.py                # Main Textual application
│   ├── script_manager.py     # Script discovery and management
│   ├── script_executor.py    # Safe script execution
│   ├── widgets/              # Reusable UI components
│   │   ├── script_list.py
│   │   ├── output_view.py
│   │   └── status_bar.py
│   └── screens/              # Application screens
│       └── main_screen.py
├── scripts/                  # User scripts directory
│   ├── config.json          # Script metadata
│   └── *.py, *.sh           # Executable scripts
├── tests/                    # Test suite
│   ├── unit/                # Unit tests
│   ├── integration/         # Integration tests
│   └── ui/                  # Textual UI tests
├── .vscode/                 # VS Code configuration
├── requirements.txt          # Production dependencies
├── requirements-dev.txt      # Development dependencies
├── pytest.ini               # Test configuration
├── .gitignore               # Git ignore rules
└── README.md               # This file
```

## Security

This application prioritizes security with multiple layers of protection:

- **Path Validation**: Prevents directory traversal attacks
- **Command Injection Prevention**: Uses subprocess safely without shell
- **Timeout Protection**: All script execution has configurable timeouts
- **Output Sanitization**: Removes dangerous escape sequences
- **Input Validation**: Validates all user inputs
- **Security Testing**: Automated security test suite
- **Dependency Scanning**: Regular vulnerability checks

See [SECURITY.md](SECURITY.md) for detailed security practices and guidelines.

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines, coding standards, and contribution workflow.

## License

[Specify license here - e.g., MIT License]

## Support

- **Issues**: Report bugs and request features via GitHub Issues
- **Discussions**: Join community discussions on GitHub Discussions
- **Documentation**: Complete API documentation available in `docs/`

---

**Built with [Textual](https://textual.textualize.io/) - A Python TUI framework**