#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

trap 'echo Fail' ERR

PLUGIN_SCHEMA="$ROOT/schemas/1.0.0/plugin.schema.json"
MCP_SCHEMA="$ROOT/schemas/1.0.0/mcp.schema.json"
VOXITY_PACKAGE="$ROOT/plugins/voxity"
IMS_PACKAGE="$ROOT/plugins/voxity-ims"

echo "Checking $VOXITY_PACKAGE/plugin.json"
npx --yes ajv-cli@5 validate --spec=draft2020 -s "$PLUGIN_SCHEMA" -d "$VOXITY_PACKAGE/plugin.json"

echo "Checking $VOXITY_PACKAGE/mcp.json"
npx --yes ajv-cli@5 validate --spec=draft2020 -s "$MCP_SCHEMA" -d "$VOXITY_PACKAGE/mcp.json"

echo "Checking $IMS_PACKAGE/plugin.json"
npx --yes ajv-cli@5 validate --spec=draft2020 -s "$PLUGIN_SCHEMA" -d "$IMS_PACKAGE/plugin.json"

echo "Checking $IMS_PACKAGE/mcp.json"
npx --yes ajv-cli@5 validate --spec=draft2020 -s "$MCP_SCHEMA" -d "$IMS_PACKAGE/mcp.json"

python3 - "$VOXITY_PACKAGE/mcp.json" "$IMS_PACKAGE/mcp.json" <<'PY'
import json
import sys
from pathlib import Path

MCP_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"
CHECKS = [
    (
        sys.argv[1],
        "voxity",
        "https://api.voxity.ai/mcp",
    ),
    (
        sys.argv[2],
        "voxity-ims",
        "https://ims.voxity.ai/mcp",
    ),
]

for path, name, url in CHECKS:
    doc = json.loads(Path(path).read_text())
    if doc.get("$schema") != MCP_SCHEMA:
        raise SystemExit(f"{path} $schema must be Agent Plugins 1.0.0")
    if set(doc.keys()) != {"$schema", "mcpServers"}:
        raise SystemExit(f"{path} may contain only $schema and mcpServers")
    if doc.get("mcpServers") != {
        name: {
            "type": "streamable-http",
            "url": url,
        }
    }:
        raise SystemExit(
            f"{path} must declare one streamable-http server named {name} at {url} with no headers"
        )
    print(f"ok singleton streamable-http {name}")
PY

for leftover in mcp bin skills/login; do
	if [[ -e "$VOXITY_PACKAGE/$leftover" ]]; then
		echo "legacy path still present: $VOXITY_PACKAGE/$leftover"
		echo Fail
		exit 1
	fi
done

shopt -s nullglob
for package in "$VOXITY_PACKAGE" "$IMS_PACKAGE"; do
	if [[ ! -e "$package/skills" ]]; then
		continue
	fi
	if [[ ! -d "$package/skills" ]]; then
		echo "skills is not a directory: $package/skills"
		echo Fail
		exit 1
	fi
	for dir in "$package"/skills/*/; do
		if [[ -f "${dir}SKILL.md" ]]; then
			echo "Checking ${dir%/}"
			npx --yes skills-ref validate "$dir"
		fi
	done
done

echo Pass
