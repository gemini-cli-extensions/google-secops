# lists all targets
list:
  just -l

# Install Google SecOps extension into Agi/Antigravity plugins directory
install-agy:
  python3 scripts/install.py


# Uninstall Google SecOps extension from Agi plugins directory
uninstall-agy:
  #!/usr/bin/env bash
  set -euo pipefail
  TARGET_DIR="$HOME/.gemini/config/plugins/google-secops"

  if [ -d "$TARGET_DIR" ] || [ -L "$TARGET_DIR" ]; then
      echo "Removing Google SecOps extension from $TARGET_DIR..."
      rm -rf "$TARGET_DIR"
      echo "Google SecOps extension has been uninstalled successfully."
  else
      echo "Google SecOps extension is not installed in $TARGET_DIR"
  fi

# Get the version from any JSON plugin/manifest file (defaults to plugin.json)
plugin-version filepath="plugin.json":
  @test/get_plugin_version.sh "{{filepath}}"

# Install Google SecOps extension into gemini CLI extensions directory
install-gemini:
  gemini extensions install https://github.com/gemini-cli-extensions/google-secops

# Claude Code: load the plugin for ONE session only (session-scoped, nothing persisted)
install-claude:
  claude --plugin-dir "{{justfile_directory()}}"

# Claude Code: install persistently via the marketplace (user scope, available in every session incl. `-p`)
install-claude-persistent:
  claude plugin marketplace add gemini-cli-extensions/google-secops
  claude plugin install google-secops@google-secops

# Run all automated validation tests
test:
  test/run_tests.sh
