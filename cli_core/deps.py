import shutil

def import_module(module_name):
    try:
        __import__(module_name)
        return True
    except ImportError as e:
        logger.error(f"Missing dependency: {module_name}")
        raise ImportError(f"Run setup.sh and and follow his instructions.")

def check_dependencies(module_dependencies: list = None, executable_dependencies: list = None):
    if executable_dependencies:
        for dependency in executable_dependencies:
            if not shutil.which(dependency):
                raise FileNotFoundError(f"{dependency} not found. Install it and try again...")
    if module_dependencies:
        for dependency in module_dependencies:
            import_module(dependency)
