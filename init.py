#!/usr/bin/env python3
"""
Initialize Python TUI project environment.
Creates virtual environment, installs dependencies, and sets up project structure.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


class Colors:
    """ANSI color codes for terminal output."""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(message: str):
    """Print a formatted header message."""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{message}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 60}{Colors.ENDC}\n")


def print_success(message: str):
    """Print a success message."""
    print(f"{Colors.OKGREEN}✓ {message}{Colors.ENDC}")


def print_info(message: str):
    """Print an info message."""
    print(f"{Colors.OKCYAN}ℹ {message}{Colors.ENDC}")


def print_warning(message: str):
    """Print a warning message."""
    print(f"{Colors.WARNING}⚠ {message}{Colors.ENDC}")


def print_error(message: str):
    """Print an error message."""
    print(f"{Colors.FAIL}✗ {message}{Colors.ENDC}")


def check_python_version():
    """Check if Python version is 3.9 or higher."""
    print_info("Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print_error(f"Python 3.9+ required, but found {version.major}.{version.minor}")
        return False
    print_success(f"Python {version.major}.{version.minor}.{version.micro} detected")
    return True


def check_venv_exists():
    """Check if virtual environment already exists."""
    venv_path = Path("venv")
    if venv_path.exists() and venv_path.is_dir():
        # Check if it's a valid venv
        if platform.system() == "Windows":
            python_exe = venv_path / "Scripts" / "python.exe"
        else:
            python_exe = venv_path / "bin" / "python"
        
        if python_exe.exists():
            print_success("Virtual environment already exists")
            return True
    return False


def create_venv():
    """Create a new virtual environment."""
    print_info("Creating virtual environment...")
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print_success("Virtual environment created successfully")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to create virtual environment: {e}")
        return False


def get_pip_executable():
    """Get the path to pip in the virtual environment."""
    venv_path = Path("venv")
    if platform.system() == "Windows":
        return str(venv_path / "Scripts" / "pip.exe")
    else:
        return str(venv_path / "bin" / "pip")


def get_python_executable():
    """Get the path to python in the virtual environment."""
    venv_path = Path("venv")
    if platform.system() == "Windows":
        return str(venv_path / "Scripts" / "python.exe")
    else:
        return str(venv_path / "bin" / "python")


def create_requirements_txt():
    """Create requirements.txt if it doesn't exist."""
    req_file = Path("requirements.txt")
    
    if req_file.exists():
        print_success("requirements.txt already exists")
        return True
    
    print_info("Creating requirements.txt...")
    
    requirements = """# TUI Framework
textual>=0.44.0
rich>=13.7.0
prompt-toolkit>=3.0.43

# Testing
pytest>=7.4.0
pytest-asyncio>=0.21.0
pytest-cov>=4.1.0
pytest-mock>=3.12.0

# Security
bandit>=1.7.5
safety>=2.3.5

# Code Quality
black>=23.12.0
isort>=5.13.0
pylint>=3.0.0
mypy>=1.7.0

# Utilities
python-dotenv>=1.0.0
"""
    
    try:
        req_file.write_text(requirements.strip())
        print_success("requirements.txt created successfully")
        return True
    except Exception as e:
        print_error(f"Failed to create requirements.txt: {e}")
        return False


def create_requirements_dev_txt():
    """Create requirements-dev.txt for development dependencies."""
    req_file = Path("requirements-dev.txt")
    
    if req_file.exists():
        print_success("requirements-dev.txt already exists")
        return True
    
    print_info("Creating requirements-dev.txt...")
    
    requirements = """# Development dependencies
ipython>=8.18.0
ipdb>=0.13.13
"""
    
    try:
        req_file.write_text(requirements.strip())
        print_success("requirements-dev.txt created successfully")
        return True
    except Exception as e:
        print_error(f"Failed to create requirements-dev.txt: {e}")
        return False


def upgrade_pip():
    """Upgrade pip to the latest version."""
    print_info("Upgrading pip...")
    pip_exe = get_pip_executable()
    try:
        subprocess.run(
            [pip_exe, "install", "--upgrade", "pip"],
            check=True,
            capture_output=True,
            text=True
        )
        print_success("pip upgraded successfully")
        return True
    except subprocess.CalledProcessError as e:
        print_warning(f"Failed to upgrade pip: {e}")
        return True  # Non-critical, continue anyway


def install_dependencies():
    """Install dependencies from requirements.txt."""
    pip_exe = get_pip_executable()
    req_file = Path("requirements.txt")
    
    if not req_file.exists():
        print_error("requirements.txt not found")
        return False
    
    print_info("Installing dependencies from requirements.txt...")
    print_info("This may take a few minutes...")
    
    try:
        subprocess.run(
            [pip_exe, "install", "-r", "requirements.txt"],
            check=True
        )
        print_success("Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to install dependencies: {e}")
        return False


def check_dependencies_installed():
    """Check if dependencies are already installed."""
    pip_exe = get_pip_executable()
    
    # Key packages to check
    key_packages = ["textual", "pytest", "bandit", "black"]
    
    try:
        result = subprocess.run(
            [pip_exe, "list"],
            capture_output=True,
            text=True,
            check=True
        )
        
        installed = result.stdout.lower()
        all_installed = all(pkg in installed for pkg in key_packages)
        
        if all_installed:
            print_success("All key dependencies already installed")
            return True
        return False
    except subprocess.CalledProcessError:
        return False


def create_directory_structure():
    """Create basic project directory structure."""
    print_info("Creating project directory structure...")
    
    directories = [
        "tui",
        "tui/widgets",
        "tui/screens",
        "scripts",
        "tests",
        "tests/unit",
        "tests/integration",
        "tests/ui",
        "tests/fixtures",
        ".opencode",
        ".opencode/prompts"
    ]
    
    for directory in directories:
        dir_path = Path(directory)
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            print_success(f"Created directory: {directory}")
        else:
            print_info(f"Directory already exists: {directory}")
    
    # Create __init__.py files
    init_files = [
        "tui/__init__.py",
        "tui/widgets/__init__.py",
        "tui/screens/__init__.py",
        "tests/__init__.py",
        "tests/unit/__init__.py",
        "tests/integration/__init__.py",
        "tests/ui/__init__.py"
    ]
    
    for init_file in init_files:
        init_path = Path(init_file)
        if not init_path.exists():
            init_path.write_text('"""Package initialization."""\n')
            print_success(f"Created: {init_file}")


def create_gitignore():
    """Create .gitignore file if it doesn't exist."""
    gitignore_path = Path(".gitignore")
    
    if gitignore_path.exists():
        print_success(".gitignore already exists")
        return
    
    print_info("Creating .gitignore...")
    
    gitignore_content = """# Virtual Environment
venv/
env/
ENV/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Project specific
*.log
.env
.env.*
bandit-report.json

# Distribution
dist/
build/
*.egg-info/
"""
    
    try:
        gitignore_path.write_text(gitignore_content.strip())
        print_success(".gitignore created successfully")
    except Exception as e:
        print_error(f"Failed to create .gitignore: {e}")


def create_pytest_ini():
    """Create pytest.ini configuration."""
    pytest_ini_path = Path("pytest.ini")
    
    if pytest_ini_path.exists():
        print_success("pytest.ini already exists")
        return
    
    print_info("Creating pytest.ini...")
    
    pytest_config = """[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --strict-markers
    --cov=tui
    --cov-report=term-missing
    --cov-report=html
    --asyncio-mode=auto
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
    ui: marks tests as UI tests
"""
    
    try:
        pytest_ini_path.write_text(pytest_config.strip())
        print_success("pytest.ini created successfully")
    except Exception as e:
        print_error(f"Failed to create pytest.ini: {e}")


def print_next_steps():
    """Print instructions for next steps."""
    print_header("Setup Complete!")
    
    print(f"{Colors.OKGREEN}Your Python TUI project is ready!{Colors.ENDC}\n")
    
    print(f"{Colors.BOLD}Next steps:{Colors.ENDC}\n")
    
    if platform.system() == "Windows":
        activate_cmd = "venv\\Scripts\\activate"
    else:
        activate_cmd = "source venv/bin/activate"
    
    print(f"  1. Activate the virtual environment:")
    print(f"     {Colors.OKCYAN}{activate_cmd}{Colors.ENDC}\n")
    
    print(f"  2. Start developing your TUI:")
    print(f"     {Colors.OKCYAN}python main.py{Colors.ENDC}\n")
    
    print(f"  3. Run tests:")
    print(f"     {Colors.OKCYAN}pytest tests/ -v{Colors.ENDC}\n")
    
    print(f"  4. Check security:")
    print(f"     {Colors.OKCYAN}bandit -r tui/ -ll{Colors.ENDC}")
    print(f"     {Colors.OKCYAN}safety check{Colors.ENDC}\n")
    
    print(f"  5. Format code:")
    print(f"     {Colors.OKCYAN}black tui/ tests/{Colors.ENDC}")
    print(f"     {Colors.OKCYAN}isort tui/ tests/{Colors.ENDC}\n")


def main():
    """Main initialization function."""
    print_header("Python TUI Project Initialization")
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check/create virtual environment
    venv_exists = check_venv_exists()
    if not venv_exists:
        if not create_venv():
            sys.exit(1)
    
    # Create requirements files
    create_requirements_txt()
    create_requirements_dev_txt()
    
    # Upgrade pip
    upgrade_pip()
    
    # Check/install dependencies
    deps_installed = check_dependencies_installed()
    if not deps_installed:
        if not install_dependencies():
            sys.exit(1)
    else:
        print_info("Skipping dependency installation (already installed)")
    
    # Create project structure
    create_directory_structure()
    create_gitignore()
    create_pytest_ini()
    
    # Print next steps
    print_next_steps()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}Initialization cancelled by user{Colors.ENDC}")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)