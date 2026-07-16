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

class BaseOperations:
    """
    Classe base extensível. O app herda esta classe para registrar
    suas próprias operações e sub-sistemas.
    """
    def __init__(self, context: Context):
        self.ctx = context
        self._dispatch_table: dict[str, callable] = {}

    def register(self, command: str, handler: callable) -> None:
        """Registra um handler para um comando."""
        self._dispatch_table[command] = handler

    def dispatch(self, command: str, args):
        """Despacha para o handler registrado."""
        handler = self._dispatch_table.get(command)
        if not handler:
            raise ValueError(f"Unknown command: {command!r}")
        return handler(args)

    def dispatch_from_context(self):
        """Atalho: lê args do context e despacha."""
        args = self.ctx.config.argparse.args
        return self.dispatch(args.command, args)

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
