# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Installation script for Google SecOps Plugin and Skills for Antigravity."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import shutil
import sys


def replace_placeholders(content: str, config: dict[str, str]) -> str:
    """Replaces ${VAR} or ${VAR:-DEFAULT} style placeholders in a string.

    Args:
        content: The input string containing template placeholders.
        config: Dictionary mapping variable names to their values.

    Returns:
        String with placeholders replaced by values from config.
    """
    pattern = re.compile(r'\$\{(\w+)(?::-(.*?))?\}')

    def replacer(match: re.Match[str]) -> str:
        var_name = match.group(1)
        default_val = match.group(2)
        if var_name in config:
            return config[var_name]
        elif default_val is not None:
            return default_val
        return match.group(0)

    return pattern.sub(replacer, content)


def read_dotenv(filepath: Path) -> dict[str, str]:
    """Parses a basic .env file into a dictionary.

    Args:
        filepath: Path to the .env file.

    Returns:
        Dictionary of key-value pairs parsed from the file.
    """
    env: dict[str, str] = {}
    if not filepath.exists():
        return env
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, val = line.split("=", 1)
                env[key.strip()] = val.strip().strip('"').strip("'")
    return env


def get_defaults() -> dict[str, str]:
    """Attempts to find existing default configurations.

    Returns:
        Dictionary of default configuration parameters.
    """
    defaults = {
        "PROJECT_ID": "secops-demo-env",
        "CUSTOMER_ID": "a13f6726-efed-452e-9008-8fe0d3cb0f75",
        "REGION": "us",
        "SERVER_URL": "https://chronicle.us.rep.googleapis.com/mcp",
    }

    # 1. Try local .env
    local_env = Path(".env")
    if local_env.exists():
        env_vars = read_dotenv(local_env)
        for k in defaults:
            if k in env_vars:
                defaults[k] = env_vars[k]

    # 2. Try legacy extensions path .env if values are still empty
    legacy_env = Path.home() / ".gemini/extensions/google-secops/.env"
    if legacy_env.exists():
        env_vars = read_dotenv(legacy_env)
        for k in defaults:
            if not defaults[k] and k in env_vars:
                defaults[k] = env_vars[k]

    return defaults


def prompt_user(defaults: dict[str, str]) -> dict[str, str]:
    """Prompts the user for config values interactively.

    Args:
        defaults: Default values to display as prompt fallbacks.

    Returns:
        Configured dictionary of parameters.
    """
    print("--------------------------------------------------")
    print("Configuring Google SecOps Plugin for Antigravity")
    print("--------------------------------------------------")

    project_id = (
        input(f"Google Cloud Project ID [{defaults['PROJECT_ID']}]: ").strip()
        or defaults["PROJECT_ID"]
    )
    while not project_id:
        project_id = input("Google Cloud Project ID (Required): ").strip()

    customer_id = (
        input(f"Chronicle Customer ID [{defaults['CUSTOMER_ID']}]: ").strip()
        or defaults["CUSTOMER_ID"]
    )
    while not customer_id:
        customer_id = input("Chronicle Customer ID (Required): ").strip()

    region = (
        input(f"Chronicle Region [{defaults['REGION']}]: ").strip()
        or defaults["REGION"]
    )
    server_url = (
        input(f"Server URL [{defaults['SERVER_URL']}]: ").strip()
        or defaults["SERVER_URL"]
    )

    return {
        "PROJECT_ID": project_id,
        "CUSTOMER_ID": customer_id,
        "REGION": region,
        "SERVER_URL": server_url,
    }


def get_target_dir(flavor: str, mode: str, project_path: str) -> Path:
    """Determines target directory based on flavor, mode, and project path.

    Args:
        flavor: Target flavor ('agy-dsk', 'ide', or 'cli').
        mode: Installation mode ('global' or 'project').
        project_path: Path to the project root directory.

    Returns:
        Path object pointing to the resolved target directory.

    Raises:
        ValueError: If flavor is unknown.
    """
    if mode == "project":
        project_root = Path(project_path).resolve()
        if flavor == "agy-dsk":
            return project_root / ".agents" / "plugins" / "google-secops"
        return project_root / ".agents" / "skills"

    # Global mode
    gemini_home = Path.home() / ".gemini"
    if flavor == "agy-dsk":
        return gemini_home / "config" / "plugins" / "google-secops"
    elif flavor == "ide":
        return gemini_home / "antigravity" / "skills"
    elif flavor == "cli":
        return gemini_home / "antigravity-cli" / "skills"

    raise ValueError(f"Unknown flavor: {flavor}")


def install_agy_dsk(
    workspace_dir: Path, target_dir: Path, config: dict[str, str]
) -> None:
    """Installs the entire plugin for the standalone AGY app.

    Args:
        workspace_dir: Path to the root workspace directory.
        target_dir: Target directory where plugin files will be copied.
        config: Configuration dictionary with environment parameters.
    """
    # Create target directory if it doesn't exist
    target_dir.mkdir(parents=True, exist_ok=True)

    print(f"Installing/updating plugin files in {target_dir}...")
    try:
        plugin_items = [
            "plugin.json",
            "skills",
            "rules",
            "agents",
            "hooks.json",
            "README.md",
        ]
        for item_name in plugin_items:
            src_item = workspace_dir / item_name
            dst_item = target_dir / item_name
            if not src_item.exists():
                continue
            if src_item.is_dir():
                if dst_item.exists():
                    shutil.rmtree(dst_item)
                shutil.copytree(
                    src_item,
                    dst_item,
                    ignore=shutil.ignore_patterns(
                        "__pycache__", "*.pyc", ".pytest_cache", ".DS_Store"
                    ),
                )
            else:
                shutil.copy2(src_item, dst_item)
    except Exception as e:
        print(f"Error copying plugin files: {e}", file=sys.stderr)
        sys.exit(1)

    # Perform variable replacement in config files
    files_to_replace = []
    for filename in files_to_replace:
        file_path = target_dir / filename
        if not file_path.exists():
            continue
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            updated_content = replace_placeholders(content, config)

            # Format JSON if it is valid JSON
            try:
                data = json.loads(updated_content)
                updated_content = json.dumps(data, indent=2)
            except json.JSONDecodeError:
                pass

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(updated_content)
        except Exception as e:
            print(
                f"Warning: Could not replace placeholders in {filename}: {e}",
                file=sys.stderr,
            )

    # Write .env file to target directory as backup
    env_path = target_dir / ".env"
    with open(env_path, "w", encoding="utf-8") as f:
        for k, v in config.items():
            f.write(f"{k}={v}\n")

    # Prepend context metadata to GEMINI.md in target directory
    gemini_md_path = target_dir / "rules/GEMINI.md"
    if gemini_md_path.exists():
        with open(gemini_md_path, "r", encoding="utf-8") as f:
            orig_content = f.read()
    else:
        orig_content = ""

    context_prefix = f"""# Google SecOps Environment Context

This file defines the configuration parameters for the Google SecOps Plugin.

*   `PROJECT_ID`: {config['PROJECT_ID']}
*   `CUSTOMER_ID`: {config['CUSTOMER_ID']}
*   `REGION`: {config['REGION']}
*   `SERVER_URL`: {config['SERVER_URL']}

---

"""
    with open(gemini_md_path, "w", encoding="utf-8") as f:
        f.write(context_prefix + orig_content)

    print(f"Standalone plugin successfully installed in {target_dir}")


def install_skills(workspace_dir: Path, target_dir: Path) -> None:
    """Installs only the skills into the skills directory for IDE or CLI.

    Args:
        workspace_dir: Path to the root workspace directory.
        target_dir: Target directory where skills will be installed.
    """
    source_skills_dir = workspace_dir / "skills"
    if not source_skills_dir.exists():
        print(
            f"Error: source skills directory not found: {source_skills_dir}",
            file=sys.stderr,
        )
        sys.exit(1)

    target_dir.mkdir(parents=True, exist_ok=True)

    for src in sorted(source_skills_dir.iterdir()):
        if src.is_dir() and not src.name.startswith(".") and (src / "SKILL.md").exists():
            skill = src.name
            dst = target_dir / skill
            print(f"Installing skill '{skill}' into {dst}...")
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)

    print(f"Skills successfully installed in {target_dir}")


def get_profile_dir(flavor: str) -> Path | None:
    """Returns the profile directory path for a given flavor.

    Args:
        flavor: Target flavor ('ide' or 'cli').

    Returns:
        Path to the profile directory, or None if unknown flavor.
    """
    gemini_home = Path.home() / ".gemini"
    if flavor == "ide":
        if (gemini_home / "antigravity-ide").exists():
            return gemini_home / "antigravity-ide"
        return gemini_home / "antigravity"
    elif flavor == "cli":
        return gemini_home / "antigravity-cli"
    return None


def install_mcp_config(
    workspace_dir: Path,
    flavor: str,
    config: dict[str, str],
    target_dir: Path | None = None,
) -> None:
    """Merges MCP server config into flavor profile or plugin mcp_config.json.

    Args:
        workspace_dir: Path to the root workspace directory.
        flavor: Target flavor ('agy-dsk', 'ide', or 'cli').
        config: Configuration dictionary with environment parameters.
        target_dir: Optional target directory (used for agy-dsk plugin directory).
    """
    profile_dir = target_dir if target_dir else get_profile_dir(flavor)
    if not profile_dir:
        print(
            "Skipping MCP config installation: No profile directory found for"
            f" flavor '{flavor}'"
        )
        return

    profile_dir.mkdir(parents=True, exist_ok=True)
    mcp_config_path = profile_dir / "mcp_config.json"

    # Read workspace source mcp_config.json template
    src_config_path = workspace_dir / "mcp_config.json"
    if not src_config_path.exists():
        print(
            "Error: Source mcp_config.json template not found in workspace.",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        with open(src_config_path, "r", encoding="utf-8") as f:
            src_content = f.read()

        # Replace placeholders
        resolved_src_content = replace_placeholders(src_content, config)
        src_data = json.loads(resolved_src_content)

        # Extract server definitions from source
        src_mcp_servers = src_data.get("mcpServers", {})
        if not src_mcp_servers:
            print(
                "Error: No mcpServers defined in mcp_config.json template.",
                file=sys.stderr,
            )
            sys.exit(1)

        # Load existing target config or start fresh
        if mcp_config_path.exists():
            with open(mcp_config_path, "r", encoding="utf-8") as f:
                target_data = json.load(f)
        else:
            target_data = {"mcpServers": {}}

        if "mcpServers" not in target_data:
            target_data["mcpServers"] = {}

        # Merge server configuration with newly resolved user settings
        for srv_name, srv_config in src_mcp_servers.items():
            target_data["mcpServers"][srv_name] = srv_config

        # Write merged config back to profile directory
        with open(mcp_config_path, "w", encoding="utf-8") as f:
            json.dump(target_data, f, indent=2)

        print(
            f"Successfully merged MCP server configuration into {mcp_config_path}"
        )
    except Exception as e:
        print(
            f"Error installing/merging MCP configuration for flavor '{flavor}': {e}",
            file=sys.stderr,
        )
        sys.exit(1)


def uninstall_flavor(
    workspace_dir: Path, target_dir: Path, flavor: str
) -> None:
    """Uninstalls plugin or skills from target_dir for a given flavor.

    Args:
        workspace_dir: Path to the root workspace directory.
        target_dir: Target directory where plugin/skills are installed.
        flavor: Target flavor ('agy-dsk', 'ide', or 'cli').
    """
    if not target_dir.exists():
        print(f"Nothing to uninstall: {target_dir} does not exist.")
        return

    if flavor == "agy-dsk":
        print(f"Removing Google SecOps plugin from {target_dir}...")
        try:
            shutil.rmtree(target_dir)
            print("Plugin successfully uninstalled.")
        except Exception as e:
            print(
                f"Error uninstalling plugin from {target_dir}: {e}",
                file=sys.stderr,
            )
    else:
        source_skills_dir = workspace_dir / "skills"
        if not source_skills_dir.exists():
            return
        removed_any = False
        for src in source_skills_dir.iterdir():
            if src.is_dir() and not src.name.startswith("."):
                dst = target_dir / src.name
                if dst.exists():
                    print(f"Removing skill '{src.name}' from {target_dir}...")
                    try:
                        shutil.rmtree(dst)
                        removed_any = True
                    except Exception as e:
                        print(f"Error removing {dst}: {e}", file=sys.stderr)
        if removed_any:
            print(f"Skills successfully uninstalled from {target_dir}.")
        else:
            print(f"No Google SecOps skills found in {target_dir}.")


def main() -> None:
    """Main CLI entry point for the installation script."""
    parser = argparse.ArgumentParser(
        description="Install Google SecOps Plugin/Skills for Antigravity."
    )
    parser.add_argument(
        "--flavor",
        default="agy-dsk",
        help="The Antigravity flavor to install for (default: agy-dsk).",
    )
    parser.add_argument(
        "--mode",
        default="global",
        help="Installation mode (default: global).",
    )
    parser.add_argument(
        "--project-path",
        default=".",
        help=(
            "Path to the project root directory (only used in project mode,"
            " default: current directory)."
        ),
    )
    parser.add_argument(
        "--uninstall",
        action="store_true",
        help="Uninstall the extension/skills for the specified flavor.",
    )

    args = parser.parse_args()

    # Normalize values if key=val formatting was passed (e.g. mode=global or project-path=.)
    if args.flavor and "=" in args.flavor:
        args.flavor = args.flavor.split("=")[-1]
    if args.mode and "=" in args.mode:
        args.mode = args.mode.split("=")[-1]
    if args.project_path and "=" in args.project_path:
        args.project_path = args.project_path.split("=")[-1]

    valid_flavors = ("agy-dsk", "ide", "cli", "all")
    if args.flavor not in valid_flavors:
        parser.error(
            f"argument --flavor: invalid choice: '{args.flavor}' (choose from"
            f" {', '.join(valid_flavors)})"
        )

    valid_modes = ("global", "project")
    if args.mode not in valid_modes:
        parser.error(
            f"argument --mode: invalid choice: '{args.mode}' (choose from"
            f" {', '.join(valid_modes)})"
        )

    workspace_dir = Path(__file__).parent.parent.resolve()
    flavors_to_install = (
        [args.flavor]
        if args.flavor != "all"
        else ["agy-dsk", "ide", "cli"]
    )

    # We prompt/config only if installing (not uninstalling) and installing standalone OR in global mode
    config = None
    if not args.uninstall and (
        "agy-dsk" in flavors_to_install or args.mode == "global"
    ):
        defaults = get_defaults()
        config = prompt_user(defaults)

    for flavor in flavors_to_install:
        target_dir = get_target_dir(flavor, args.mode, args.project_path)
        if args.uninstall:
            print(
                f"\n--- Uninstalling flavor '{flavor}' ({args.mode} mode) ---"
            )
            uninstall_flavor(workspace_dir, target_dir, flavor)
        else:
            print(f"\n--- Installing flavor '{flavor}' ({args.mode} mode) ---")
            if flavor == "agy-dsk":
                install_agy_dsk(workspace_dir, target_dir, config)
                if config:
                    install_mcp_config(
                        workspace_dir, flavor, config, target_dir
                    )
            else:
                install_skills(workspace_dir, target_dir)
                if args.mode == "global" and config:
                    install_mcp_config(workspace_dir, flavor, config)


if __name__ == "__main__":
    main()
