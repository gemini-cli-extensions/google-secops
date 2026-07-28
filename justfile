# List all available targets
list:
  just -l

# Install plugin for Antigravity Desktop
install-agy-dsk mode="global" path=".":
  python3 scripts/install.py --flavor=agy-dsk --mode={{mode}} --project-path={{path}}

# Install skills for Antigravity IDE
install-agy-ide mode="global" path=".":
  python3 scripts/install.py --flavor=ide --mode={{mode}} --project-path={{path}}

# Install skills for Antigravity CLI
install-agy-cli mode="global" path=".":
  python3 scripts/install.py --flavor=cli --mode={{mode}} --project-path={{path}}

# Install for all Antigravity flavors (Desktop, IDE, CLI)
install-agy-all mode="global" path=".":
  python3 scripts/install.py --flavor=all --mode={{mode}} --project-path={{path}}



# Uninstall plugin for Antigravity Desktop
uninstall-agy-dsk mode="global" path=".":
  python3 scripts/install.py --flavor=agy-dsk --uninstall --mode={{mode}} --project-path={{path}}

# Uninstall skills for Antigravity IDE
uninstall-agy-ide mode="global" path=".":
  python3 scripts/install.py --flavor=ide --uninstall --mode={{mode}} --project-path={{path}}

# Uninstall skills for Antigravity CLI
uninstall-agy-cli mode="global" path=".":
  python3 scripts/install.py --flavor=cli --uninstall --mode={{mode}} --project-path={{path}}

# Uninstall from all Antigravity flavors
uninstall-agy-all mode="global" path=".":
  python3 scripts/install.py --flavor=all --uninstall --mode={{mode}} --project-path={{path}}

# Uninstall Antigravity extension (alias for uninstall-agy-all)
uninstall-agy mode="global" path=".":
  python3 scripts/install.py --flavor=all --uninstall --mode={{mode}} --project-path={{path}}

# Get plugin version from manifest
plugin-version file="plugin.json":
  @test/get_plugin_version.sh "{{file}}"

# Install extension for Gemini CLI
install-gemini:
  gemini extensions install https://github.com/gemini-cli-extensions/google-secops

# Install plugin for Claude Code
install-claude mode="global":
  #!/usr/bin/env bash
  set -euo pipefail
  if [ "{{mode}}" = "global" ]; then
      claude plugin marketplace add gemini-cli-extensions/google-secops
      claude plugin install google-secops@google-secops
  elif [ "{{mode}}" = "local" ] || [ "{{mode}}" = "project" ] || [ "{{mode}}" = "session" ]; then
      claude --plugin-dir "{{justfile_directory()}}"
  else
      echo "Error: Unknown mode '{{mode}}'. Valid options are: global, local, project, session." >&2
      exit 1
  fi

# Run automated validation test suite
test:
  test/run_tests.sh
