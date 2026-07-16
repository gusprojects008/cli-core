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