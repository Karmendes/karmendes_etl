#!/bin/bash

set -e  # Exit on error

# Detect OS
OS=$(uname -s)

# Validate virtualenv name
if [ $# -eq 0 ]; then
  echo "⚠️  Please provide a name for the virtual environment."
  echo "Example: bash setup.sh venv"
  exit 1
fi

virtualenv_name=$1

# Function to check if a command exists
command_exists() {
  command -v "$1" >/dev/null 2>&1
}

# Check for Python
echo "🔍 Checking for Python..."
if command_exists python3; then
  PYTHON_CMD="python3"
elif command_exists python; then
  PYTHON_CMD="python"
else
  echo "❌ Python is not installed."

  if [[ "$OS" == "Darwin" ]]; then
    echo "🍎 Installing Python with Homebrew..."
    if ! command_exists brew; then
      echo "❌ Homebrew not found. Please install Homebrew first: https://brew.sh/"
      exit 1
    fi
    brew install python
    PYTHON_CMD="python3"
  elif [[ "$OS" == "Linux" ]]; then
    echo "🐧 Installing Python with apt..."
    sudo apt update
    sudo apt install -y python3 python3-venv python3-pip
    PYTHON_CMD="python3"
  else
    echo "⚠️  Automatic Python installation is not supported for this OS. Please install Python manually."
    exit 1
  fi
fi

# Ensure pip is available
echo "🔧 Ensuring pip is available..."
$PYTHON_CMD -m ensurepip --upgrade

# Check for git
echo "🔍 Checking for git..."
if ! command_exists git; then
  echo "❌ git is not installed."
  
  if [[ "$OS" == "Darwin" ]]; then
    echo "🍎 Installing git with Homebrew..."
    brew install git
  elif [[ "$OS" == "Linux" ]]; then
    echo "🐧 Installing git with apt..."
    sudo apt update
    sudo apt install -y git
  else
    echo "⚠️  Automatic git installation is not supported for this OS. Please install git manually."
    exit 1
  fi
fi

# Check and install virtualenv
echo "🔍 Checking for virtualenv..."
if ! command_exists virtualenv; then
  echo "⚙️  Installing virtualenv with pip..."
  $PYTHON_CMD -m pip install --upgrade pip
  $PYTHON_CMD -m pip install virtualenv
fi

# Create virtual environment
echo "🚀 Creating virtual environment '$virtualenv_name'..."
$PYTHON_CMD -m virtualenv "$virtualenv_name"

# Activate based on OS
echo "⚙️  Activating virtual environment..."
case "$OS" in
  Darwin|Linux)
    source "./$virtualenv_name/bin/activate"
    ;;
  MINGW*|MSYS*|CYGWIN*)
    source "./$virtualenv_name/Scripts/activate"
    ;;
  *)
    echo "Unsupported OS: $OS"
    exit 1
    ;;
esac

# .gitignore setup
echo "📝 Configuring .gitignore..."
{
  echo "**/__pycache__"
  echo "$virtualenv_name"
} >> .gitignore

# Install project dependencies
echo "📦 Installing pylint and pre-commit..."
pip install --upgrade pip
pip install pylint pre-commit

# Generate pylint config
echo "⚙️  Generating .pylintrc..."
pylint --generate-rcfile > .pylintrc

# VSCode config
echo "🛠️  Setting up VSCode..."
mkdir -p .vscode
cat <<EOF > .vscode/settings.json
{
  "python.linting.pylintEnabled": true,
  "python.linting.enabled": true,
  "files.exclude": {
    "**/*.pyc": { "when": "\$(basename).py" },
    "**/__pycache__": true,
    "**/*.pytest_cache": true
  }
}
EOF

# Pre-commit config
echo "🔧 Setting up pre-commit hooks..."
cat <<EOF > .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: pylint
        name: pylint
        entry: pylint
        language: system
        types: [python]
        args:
          [
            "-rn",
            "-sn",
            "--rcfile=.pylintrc",
            "--load-plugins=pylint.extensions.docparams"
          ]
  - repo: local
    hooks:
      - id: requirements
        name: requirements
        entry: bash -c 'pip freeze > requirements.txt; git add requirements.txt'
        language: system
        pass_filenames: false
        stages: [commit]
EOF

pre-commit install

echo "✅ Setup completed successfully!"

