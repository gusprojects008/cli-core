#!/usr/bin/env bash

set -euo pipefail

RESET='\033[0m'

BOLD='\033[1m'
DIM='\033[2m'
UNDERLINE='\033[4m'
REVERSE='\033[7m'

RED='\033[31m'
YELLOW='\033[33m'
GREEN='\033[32m'
BLUE='\033[34m'
CYAN='\033[36m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

PROJECT_NAME="yourproject"

VENV_DIR=".venv"
VENV_PATH="$SCRIPT_DIR/$VENV_DIR"

VENV_PYTHON="$VENV_PATH/bin/python"
VENV_ARGCOMPLETE="$VENV_PATH/bin/register-python-argcomplete"

EXECUTABLES=(
    "yourproject"
    "yourproject-tui"
)

CURRENT_SHELL=$(basename "$SHELL")

case "$CURRENT_SHELL" in
    bash)
        RC_FILE="$HOME/.bashrc"
        ;;
    zsh)
        RC_FILE="$HOME/.zshrc"
        ;;
    *)
        RC_FILE=""
        ;;
esac

print_step() {
    echo
    echo "==> $1"
}

print_ok() {
    echo "✔ $1"
}

print_error() {
    echo "✖ $1"
    exit 1
}

print_header() {
    echo
    echo -e "${REVERSE} $1 ${RESET}"
    echo
}

print_section() {
    echo -e "${BOLD}$1:${RESET}"
}

print_info() {
    echo -e "  ${BLUE}$1${RESET}"
}

print_success() {
    echo -e "  ${GREEN}$1${RESET}"
}

print_warning() {
    echo -e "  ${YELLOW}$1${RESET}"
}

print_error_msg() {
    echo -e "  ${RED}$1${RESET}"
}

print_command() {
    echo -e "  ${GREEN}$1${RESET}"
}

print_comment() {
    echo -e "  ${DIM}# $1${RESET}"
}

print_separator_smooth() {
    local cols
    cols=$(tput cols 2>/dev/null || echo 80)
    printf "%*s\n" "$cols" "" | tr ' ' '─'
}

print_separator_equals() {
    local cols
    cols=$(tput cols 2>/dev/null || echo 80)
    printf "%*s\n" "$cols" "" | tr ' ' '='
}

get_venv_executable() {
    local executable="$1"
    echo "$VENV_PATH/bin/$executable"
}

create_wrapper() {
    local executable="$1"

    local venv_executable
    venv_executable=$(get_venv_executable "$executable")

    local wrapper_path="/usr/local/bin/$executable"

    local wrapper_content
    wrapper_content="#!/usr/bin/env bash
exec \"$venv_executable\" \"\$@\""

    print_step "Creating wrapper for '$executable'..."

    if echo "$wrapper_content" | sudo tee "$wrapper_path" > /dev/null; then
        sudo chmod +x "$wrapper_path"
        print_ok "Wrapper created at $wrapper_path"
    else
        print_error_msg "Failed to create wrapper for '$executable'"
        exit 1
    fi
}

configure_autocomplete() {
    local executable="$1"

    local autocomplete_line
    autocomplete_line="eval \"\$($VENV_ARGCOMPLETE $executable)\""

    if [ -z "$RC_FILE" ]; then
        print_warning "Shell '$CURRENT_SHELL' not supported for automation."
        print_info "Manually add the following to your shell configuration file:"
        print_command "$autocomplete_line"
        return
    fi

    if grep -q "# $executable autocomplete" "$RC_FILE"; then
        print_warning "Autocomplete already configured for '$executable'"
        return
    fi

    {
        echo ""
        echo "# $executable autocomplete"

        if [[ "$CURRENT_SHELL" == "zsh" ]]; then
            echo "autoload -U bashcompinit && bashcompinit"
        fi

        echo "$autocomplete_line"
    } >> "$RC_FILE"

    print_ok "Autocomplete added for '$executable'"
}

print_step "Setting up virtual environment..."

if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
    print_ok "Virtual environment created."
else
    print_ok "Virtual environment already exists."
fi

source "$VENV_DIR/bin/activate"

print_step "Upgrading pip..."
python -m pip install --upgrade pip >/dev/null 2>&1

print_step "Installing dependencies..."

if ! pip install -e . --no-cache-dir --no-input --upgrade --force-reinstall; then
    print_error "Failed to install dependencies"
fi

print_step "Setup completed successfully!"

print_header "${RED} IMPORTANT"

print_section "Interpreter"
print_info "$VENV_PYTHON"
echo

print_section "Virtual environment"

print_comment "activate virtual environment"
print_command "source \"$VENV_DIR/bin/activate\""
echo

print_section "Executables"

for executable in "${EXECUTABLES[@]}"; do
    executable_path=$(get_venv_executable "$executable")

    print_comment "run $executable"
    print_command "\"$executable_path\" --help"
    echo
done

print_header "${CYAN} OPTIONAL: CREATE WRAPPERS + AUTOCOMPLETE"

read -p "Do you want to expose executables globally with autocomplete? (requires sudo) (y/n) " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    if [ ! -f /usr/share/bash-completion/bash_completion ]; then
        print_warning "bash-completion not found (optional)"
    fi

    if [ ! -f "$VENV_ARGCOMPLETE" ]; then
        print_error_msg "argcomplete not found in venv."
        print_command "Run: source \"$VENV_DIR/bin/activate\" && pip install argcomplete"
        exit 1
    fi

    for executable in "${EXECUTABLES[@]}"; do
        create_wrapper "$executable"
        configure_autocomplete "$executable"
    done

    if [ -n "$RC_FILE" ]; then
        print_header "${RED} IMPORTANT"

        print_section "To activate"
        print_command "source \"$RC_FILE\""
        echo
    fi

    print_section "Usage"

    for executable in "${EXECUTABLES[@]}"; do
        print_command "$executable --help"
    done

    echo
else
    print_info "Skipped wrapper installation."

    print_section "Run directly from venv"

    for executable in "${EXECUTABLES[@]}"; do
        executable_path=$(get_venv_executable "$executable")
        print_command "\"$executable_path\" --help"
    done

    echo
fi

print_ok "Setup complete!"
