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

import os
import sys
import shutil
import subprocess
import json
from pathlib import Path

def read_dotenv(filepath):
    """Parses a basic .env file into a dictionary."""
    env = {}
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

def get_defaults():
    """Attempts to find existing default configurations."""
    defaults = {
        "PROJECT_ID": "secops-demo-env",
        "CUSTOMER_ID": "a13f6726-efed-452e-9008-8fe0d3cb0f75",
        "REGION": "us",
        "SERVER_URL": "https://chronicle.us.rep.googleapis.com/mcp"
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

def prompt_user(defaults):
    """Prompts the user for config values interactively."""
    print("--------------------------------------------------")
    print("Configuring Google SecOps Plugin for Antigravity")
    print("--------------------------------------------------")
    
    project_id = input(f"Google Cloud Project ID [{defaults['PROJECT_ID']}]: ").strip() or defaults['PROJECT_ID']
    while not project_id:
        project_id = input("Google Cloud Project ID (Required): ").strip()
        
    customer_id = input(f"Chronicle Customer ID [{defaults['CUSTOMER_ID']}]: ").strip() or defaults['CUSTOMER_ID']
    while not customer_id:
        customer_id = input("Chronicle Customer ID (Required): ").strip()
        
    region = input(f"Chronicle Region [{defaults['REGION']}]: ").strip() or defaults['REGION']
    server_url = input(f"Server URL [{defaults['SERVER_URL']}]: ").strip() or defaults['SERVER_URL']
    
    return {
        "PROJECT_ID": project_id,
        "CUSTOMER_ID": customer_id,
        "REGION": region,
        "SERVER_URL": server_url
    }

def main():
    target_dir = Path.home() / ".gemini/config/plugins/google-secops"
    
    # Pre-checks
    if target_dir.exists():
        print(f"Directory {target_dir} already exists.")
        overwrite = input("Do you want to reconfigure/overwrite it? (y/n): ").strip().lower()
        if overwrite != 'y':
            print("Installation cancelled.")
            sys.exit(0)
            
    defaults = get_defaults()
    config = prompt_user(defaults)
    
    # Create config directory if needed
    plugins_base_dir = Path.home() / ".gemini/config/plugins"
    plugins_base_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy workspace files to target directory
    workspace_dir = Path(__file__).parent.parent
    
    if target_dir.exists():
        shutil.rmtree(target_dir)
        
    print(f"Installing google-secops into {target_dir}...")
    try:
        shutil.copytree(
            workspace_dir,
            target_dir,
            ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc", ".pytest_cache", ".DS_Store", ".env", ".env.*")
        )
    except Exception as e:
        print(f"Error copying plugin files: {e}", file=sys.stderr)
        sys.exit(1)
        
    # Read mcp_config.json template from workspace or target dir
    template_path = target_dir / "mcp_config.json"
    if not template_path.exists():
        print(f"Error: mcp_config.json not found in target repository.", file=sys.stderr)
        sys.exit(1)
        
    with open(template_path, "r", encoding="utf-8") as f:
        mcp_data = json.load(f)
        
    # Perform variable replacement in JSON
    mcp_str = json.dumps(mcp_data)
    mcp_str = mcp_str.replace("${SERVER_URL}", config["SERVER_URL"])
    mcp_str = mcp_str.replace("${PROJECT_ID}", config["PROJECT_ID"])
    mcp_str = mcp_str.replace("${CUSTOMER_ID}", config["CUSTOMER_ID"])
    mcp_str = mcp_str.replace("${REGION}", config["REGION"])
    
    # Write updated mcp_config.json to target
    with open(template_path, "w", encoding="utf-8") as f:
        f.write(json.dumps(json.loads(mcp_str), indent=2))
        
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
        
    # Copy template configs if any
    print(f"Google SecOps extension successfully installed in {target_dir}")

if __name__ == "__main__":
    main()
