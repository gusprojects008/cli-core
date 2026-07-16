This file is a merged representation of a subset of the codebase, containing files not matching ignore patterns, combined into a single document by Repomix.

# File Summary

## Purpose
This file contains a packed representation of a subset of the repository's contents that is considered the most important context.
It is designed to be easily consumable by AI systems for analysis, code review,
or other automated processes.

## File Format
The content is organized as follows:
1. This summary section
2. Repository information
3. Directory structure
4. Repository files (if enabled)
5. Multiple file entries, each consisting of:
  a. A header with the file path (## File: path/to/file)
  b. The full contents of the file in a code block

## Usage Guidelines
- This file should be treated as read-only. Any changes should be made to the
  original repository files, not this packed version.
- When processing this file, use the file path to distinguish
  between different files in the repository.
- Be aware that this file may contain sensitive information. Handle it with
  the same level of security as you would the original repository.

## Notes
- Some files may have been excluded based on .gitignore rules and Repomix's configuration
- Binary files are not included in this packed representation. Please refer to the Repository Structure section for a complete list of file paths, including binary files
- Files matching these patterns are excluded: .**, docs, tests
- Files matching patterns in .gitignore are excluded
- Files matching default ignore patterns are excluded
- Files are sorted by Git change count (files with more changes are at the bottom)

# Directory Structure
```
cli_core/
  __init__.py
  __main__.py
  app.py
  deps.py
  files.py
  log.py
  system.py
templates/
  python/
    docs/
      ARCHITECTURE.md
      cli-core.md
    src/
      packagename/
        app/
          app.py
        __init__.py
        __main__.py
    tests/
      test.py
    .gitignore
    main.py
    pyproject.toml
    README.md
    setup.sh
LICENSE
pyproject.toml
README.md
```

# Files

## File: cli_core/app.py
```python
"""
An auxiliary module that allows applications to be initialized in a safer and more user-friendly way, preventing dependency errors, 
and providing execution context for other functions. This context provides environment variable data, application configuration, etc.
"""

"""
Application runtime infrastructure dealing with sandboxed execution environments and logging paths.
"""

import os
import pwd
from pathlib import Path
from logging import getLogger
from dataclasses import dataclass
from argparse import ArgumentParser, Namespace
from cli_core.deps import check_dependencies

logger = getLogger(__name__)

@dataclass
class ArgparseConfig:
    parser: ArgumentParser | None = None
    args: Namespace | None = None 

@dataclass
class Config:
    """
    Generic base configuration schema for the client application.
    Developers should expand this dataclass with application-specific properties.
    """
    system_deps: list[str] | None = None
    module_deps: list[str] | None = None
    argparse: ArgparseConfig | None = None

class Context:
    """
    Encapsulates application directories, permissions, and runtime states.
    
    Attributes:
        real_user (str): Resolved physical host username, accurately supporting SUDO elevation.
        home_dir (Path): Absolute filesystem location pointing to user home.
        config_dir (Path): Dynamic custom configuration storage path (~/.config/app).
        cache_dir (Path): App-specific isolated layout directory (~/.cache/app).
        log_file (Path): Absolute endpoint pointer targeting the framework log file.
    """
    
    def __init__(self, config: Config, log_fullpath: Path, app_name: str):
        self.config = config or {}
        
        # Safely capture caller name when executed with sudo context wrapper
        self.real_user = os.environ.get("SUDO_USER") or os.getlogin()
        pw = pwd.getpwnam(self.real_user)
        self.home_dir = Path(pw.pw_dir)
        
        # Enforce secured runtime sandbox zones on physical directories
        self.config_dir = self.home_dir / ".config" / app_name
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config_dir.chmod(0o740)
        
        self.cache_dir = self.home_dir / ".cache" / app_name
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_dir.chmod(0o740)
        
        self.log_file = log_file or (self.cache_dir / f"{app_name}.log")
        
        logger.debug(
            f"Context sandbox initialized: user={self.real_user}, "
            f"config_dir={self.config_dir}, cache_dir={self.cache_dir}"
        )

class Operations:
    """
    Main execution engine responsible for executing core business operations.
    """
    def __init__(self, context):
        self.context = context
        self.logger = context.logger if hasattr(context, 'logger') else None

    def run(self):
        """
        Primary entry point loop or procedure triggered by the binary runner.
        """
        if self.logger:
            self.logger.info("Application execution runtime started successfully.")
        print("Hello from your newly scaffolded generic application!")

    def 

@dataclass
class BootstrapResult:
    """
    Data capsule storing initialized execution runtime parameters.
    """
    context: object
    operations: object

def bootstrap(config: AppConfig) -> BootstrapResult:
    """
    Validates framework dependencies, provisions the environment logger, 
    and initializes execution state.
    """
    module_deps = config.module_deps
    system_deps = config.system_deps

    # Ensure all baseline binary and code dependencies are present
    check_dependencies(module_dependencies, system_dependencies)

    from cli_core.log import setup_logging, build_logging_config

    # Setup the logging architecture from input arguments or fallback to default pathing
    if config.argparse:
        args = config.argparse.args
        logging_config = build_logging_config(args.verbose, args.output)
        log_filepath = setup_logging(logging_config=logging_config)
    else:
        log_filepath = setup_logging(verbose=True, output_path="app-debug.log")

    config["log_filepath"] = log_filepath

    # Instantiate runtime contexts
    context = Context(config)
    operations = Operations(context)

    return BootstrapResult(context, operations)
```

## File: templates/python/docs/ARCHITECTURE.md
```markdown
# cli-core Architecture Documentation

# Devisões de arquitetura pendentes:

## Padrões do projeto que é aconselhavel/recomendável serem seguidos
```

## File: templates/python/src/packagename/app/app.py
```python
from cli_core.app import Config

def make_config() -> Config:
    # It populates the standard AppConfig dataclass structure that cli_core provides.
    config = Config()
    config.custom1 = {}
    config.custom2 = {}
    return config
```

## File: templates/python/src/packagename/__init__.py
```python

```

## File: templates/python/src/packagename/__main__.py
```python

```

## File: templates/python/tests/test.py
```python
import time
import json
import threading
from logging import getLogger
from packagename.bootstrap import init

config = {
    "module_dependencies": ["c", "b", "c"],
    "system_dependencies": ["d", "e"],
    "argparse": {}
}

result = init(config)
operations = result.operations

ENABLE_SYSTEM_TESTS = True
RUN_ALL = False
INTERACTIVE_MODE = True

logger = getLogger(__name__)

def run_test(name: str, func, *args, **kwargs):
    if not should_run_test(name):
        logger.info(f"[SKIPPED] {name}")
        return

    logger.info(f"\n[TEST START] {name}")
    try:
        result = func(*args, **kwargs)
        logger.info(f"[TEST OK] {name} {result}")
        return result
    except Exception as e:
        logger.error(f"[TEST FAIL] {name}: {e}", exc_info=True)
    finally:
        logger.info(f"[TEST END] {name}\n")

def run_blocking_test(name: str, func, timeout: float = 10, **kwargs):
    if not should_run_test(name):
        logger.info(f"[SKIPPED] {name}")
        return

    logger.info(f"\n[TEST START] {name}")

    stop_event = threading.Event()

    def target():
        try:
            func(timeout=timeout, stop_event=stop_event, **kwargs)
        except Exception as e:
            logger.error(f"[THREAD ERROR] {name}: {e}", exc_info=True)

    thread = threading.Thread(target=target, daemon=True)
    thread.start()

    try:
        thread.join(timeout)

        if thread.is_alive():
            logger.warning(f"[TIMEOUT] {name} exceeded {timeout}s, stopping...")
            stop_event.set()
            thread.join(2)

    except KeyboardInterrupt:
        logger.warning(f"[INTERRUPTED] {name} (Ctrl+C)")
        stop_event.set()
        thread.join(2)

    logger.info(f"[TEST END] {name}\n")

def should_run_test(name: str) -> bool:
    global RUN_ALL

    if not INTERACTIVE_MODE or RUN_ALL:
        return True

    choice = input(f"Run test '{name}'? [y/n/a]: ").strip().lower()

    if choice == "a":
        RUN_ALL = True
        return True

    return choice in ("y", "yes")

def run_tests():
    run_test(
        "operation1 example",
        operations.operation1,
        test=True,
    )

    if ENABLE_SYSTEM_TESTS:
        logger.warning("SYSTEM TESTS ENABLED — this will modify system/network state")

        run_test(
            "operation2  [ENABLED SYSTEM TESTS]",
            operations.operation2
        )

        run_blocking_test(
            "operation3 (live test)",
            operations.operation3
        )

    else:
        logger.info("System tests disabled")

def main():
    run_tests()

if __name__ == "__main__":
    main()
```

## File: templates/python/pyproject.toml
```toml
[project]
name = "{{ project_name }}"
version = "0.1.0"
description = "CLI application built on top of cli-core framework"
readme = "README.md"
requires-python = ">=3.10"
authors = [
    {name = "Developer", email = "dev@example.com"}
]
dependencies = [
    "cli-core"
]

[build-system]
requires = ["setuptools>=61.0.0"]
build-backend = "setuptools.build_meta"

[tool.setuptools]
packages = ["{{ package_name }}"]
```

## File: cli_core/__init__.py
```python

```

## File: cli_core/__main__.py
```python
"""
Multi-template scaffolding engine for the cli-core framework ecosystem.
"""

import sys
import argparse
from pathlib import Path
from importlib.resources import files

try:
    from jinja2 import Template
    HAS_JINJA = True
except ImportError:
    HAS_JINJA = False

def render_content(content: str, context: dict) -> str:
    """
    Renders template layout string targeting variables via Jinja2 or fallback replacement rules.
    """
    if HAS_JINJA:
        return Template(content).render(context)
    else:
        # Secure basic substitution string mechanics if Jinja2 is absent
        modified = content.replace("{{ project_name }}", context["project_name"])
        modified = modified.replace("{{ package_name }}", context["package_name"])
        return modified

def create_app(project_name: str, template_type: str):
    """
    Scaffolds a clean application package workspace driven by a specific language/runtime template type.
    """
    # Standardize target names for package references and variables
    package_name = project_name.lower().replace("-", "_").replace(" ", "_")
    output_dir = Path.cwd() / project_name
    
    if output_dir.exists():
        print(f"Error: Target installation directory '{project_name}' already exists.", file=sys.stderr)
        sys.exit(1)

    print(f"Initializing generic scaffolding for '{project_name}' using template variant '{template_type}'...")

    try:
        # Dynamically locate the template subdirectory based on the type argument provided
        template_base = files("cli_core").joinpath(f"templates/{template_type}")
        
        # Enforce strict validation ensuring the target template resource layout actually exists
        if not template_base.exists():
            print(f"Error: Template type '{template_type}' is not supported by this framework version.", file=sys.stderr)
            sys.exit(1)
            
    except Exception as e:
        print(f"Failed to resolve built-in resource templates: {e}", file=sys.stderr)
        sys.exit(1)
    
    context = {
        "project_name": project_name,
        "package_name": package_name
    }

    def copy_tree(template_path, current_output):
        current_output.mkdir(parents=True, exist_ok=True)
        
        for item in template_path.iterdir():
            item_name = item.name
            # Map generic core indicators directly to the target snake_case package name string
            if item_name == "packagename":
                item_name = package_name
                
            target_path = current_output / item_name
            
            if item.is_dir():
                if item.name == "__pycache__":
                    continue
                copy_tree(item, target_path)
            else:
                content = item.read_text(encoding="utf-8")
                rendered = render_content(content, context)
                target_path.write_text(rendered, encoding="utf-8")

    copy_tree(Path(str(template_base)), output_dir)
    print(f"Success! Client package generated with template architecture '{template_type}' at: {output_dir}")

def main():
    """
    Main developer entrypoint intercepting instructions for environment setup and project generation.
    """
    parser = argparse.ArgumentParser(description="cli-core multi-runtime system development toolchain")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    init_parser = subparsers.add_parser("init", help="Generate code layouts from structural templates")
    init_parser.add_argument("name", help="Name indicator string targeting your new application artifact")
    init_parser.add_argument(
        "-t", "--type", 
        default="python", 
        help="Specify target development stack archetype pattern template (e.g., 'python')"
    )
    
    args = parser.parse_args()
    if args.command == "init":
        create_app(args.name, args.type)

if __name__ == "__main__":
    main()
```

## File: cli_core/system.py
```python
import os
import sys

def check_root():
    if os.geteuid() != 0:
        raise PermissionError(
            f"Run as root: sudo {' '.join(sys.argv)}"
        )
```

## File: templates/python/docs/cli-core.md
```markdown
## Ideias e implementações futuras 
Esta seção contém percepções coletadas durante o desenvolvimento; nenhuma está garantida para ser implementada. Elas exigem revisão e pesquisa adicional.

## O que está faltando? para corrigir / adicionar

## Melhorias e correções durante o projeto (pode ser utilizado no release)

## Explicações e esclarecimentos

## Referências

## Desabafos durante todo o projeto kkkkkkk
```

## File: templates/python/.gitignore
```

```

## File: templates/python/README.md
```markdown

```

## File: LICENSE
```
MIT License

Copyright (c) 2026 Gustavo Araújo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## File: README.md
```markdown
# cli-core
A package containing common, generic, and reusable functions for developing CLI applications.
```

## File: cli_core/files.py
```python
import time
import json
from pathlib import Path

def new_file_path(path: str | Path = None, fallback="output"):
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    p = Path(path if path else fallback)
    return p.with_name(f"{p.stem}-{timestamp}{p.suffix}")

def iter_json_objects(path: str | Path):
    is_jsonl = str(path).lower().endswith(".jsonl")

    with open(path, "r", encoding="utf-8") as file:
        if is_jsonl:
            for line_num, line in enumerate(file, start=1):
                line = line.strip()
                if not line:
                    continue
                try:
                    yield json.loads(line)
                except json.JSONDecodeError as error:
                    raise ValueError(f"Error decoding JSONL at line {line_num}: {error}")
        else:
            content = file.read()
            try:
                yield json.loads(content)
            except json.JSONDecodeError:
                decoder = json.JSONDecoder()
                idx = 0
                length = len(content)

                while idx < length:
                    while idx < length and content[idx].isspace():
                        idx += 1
                    if idx >= length:
                        break

                    try:
                        obj, idx = decoder.raw_decode(content, idx)
                        yield obj
                    except json.JSONDecodeError:
                        break

def walk_json(data, extractor: callable):
    if isinstance(data, dict):
        yield from extractor(data)
        for value in data.values():
            yield from walk_json(value, extractor)

    elif isinstance(data, list):
        for item in data:
            yield from walk_json(item, extractor)

def iter_from_json(
    path: str | Path,
    extractor: callable
):
    try:
        for obj in iter_json_objects(path):
            yield from walk_json(obj, extractor)
    except Exception as error:
        raise RuntimeError(f"Could not process file {path}: {error}")
```

## File: cli_core/deps.py
```python
import shutil

def import_module(module_name):
    try:
        __import__(module_name)
        return True
    except ImportError as e:
        raise ImportError(f"Missing dependency: {module_name}\nRun setup.sh and and follow his instructions.")

def check_dependencies(module_dependencies: list = None, system_dependencies: list = None):
    if system_dependencies:
        for dependency in system_dependencies:
            if not shutil.which(dependency):
                raise FileNotFoundError(f"{dependency} not found. Install it and try again...")
    if module_dependencies:
        for dependency in module_dependencies:
            import_module(dependency)
```

## File: pyproject.toml
```toml
[project]
name = "cli-core"
version = "1.0.0"
description = "Reusable CLI utilities"
authors = [{name = "Gustavo Araújo"}]
dependencies = ["rich"]

[build-system]
requires = ["setuptools"]
build-backend = "setuptools.build_meta"

[tool.setuptools]
packages = ["cli_core"]

[tool.setuptools.package-data]
"cli_core" = ["../templates/**/*"]

[project.scripts]
cli-core = "cli_core.__main__:main"
```

## File: templates/python/main.py
```python
from cli_core.app import bootstrap
from {{ mypackage }} import app

def main():
    config = app.make_config()
    """ 
    Se for uma aplicação CLI posso definir argparse.args e argparse.parser para o resultado de config:
    parser = parse_args()
    args = parser.parse_args()
    config.argparse.parser = parser
    config.argparse.args = args
    """
    bootstrap_result = bootstrap(config)
    """
    Se for aplicação CLI, é possível fazer:
    bootstrap_result.operations.dispatch()
    """
```

## File: templates/python/setup.sh
```bash
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
```

## File: cli_core/log.py
```python
import logging
import logging.config
from logging import Formatter, FileHandler
from pathlib import Path
from cli_core.files import new_file_path

DEFAULT_PATH = "debug.log"

def build_logging_config(verbose: bool = False, output: Path | str = None):
    handlers = {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "simple",
        }
    }

    formatters = {
        "simple": {
            "format": "%(message)s"
        },
        "detailed": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        }
    }

    try:
        import rich.logging

        handlers["console"] = {
            "class": "rich.logging.RichHandler",
            "level": "INFO",
            "formatter": "simple",
            "rich_tracebacks": True,
            "show_time": False,
            "show_path": False,
        }
    except ImportError:
        pass

    root_handlers = ["console"]

    if verbose:
        logfile = str(new_file_path(output, DEFAULT_PATH))

        handlers["file"] = {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "detailed",
            "filename": logfile,
        }

        root_handlers.append("file")

    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": formatters,
        "handlers": handlers,
        "root": {
            "level": "DEBUG",
            "handlers": root_handlers,
        },
    }

def setup_logging(
    verbose: bool = False,
    output_path: Path | str = None,
    logging_config: dict | None = None
):
    if isinstance(logging_config, dict):
        if not logging_config:
            raise ValueError("logging_config cannot be empty")
        logging.config.dictConfig(logging_config)
        return

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    try:
        from rich.logging import RichHandler

        console = RichHandler(
            rich_tracebacks=True,
            show_time=False,
            show_path=False
        )
    except ImportError:
        console = logging.StreamHandler()

    console.setLevel(logging.INFO)
    console.setFormatter(Formatter("%(message)s"))
    logger.addHandler(console)

    if verbose:
        file_handler = FileHandler(str(new_file_path(output_path, DEFAULT_PATH)))
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(
            Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
        )
        logger.addHandler(file_handler)
```
