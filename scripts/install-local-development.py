#!/usr/bin/env python3
"""Copy DEV packages into Cursor's local plugins directory with unique names."""

import json
from pathlib import Path
import re
import shutil
import tempfile


ROOT = Path(__file__).resolve().parents[1]
PRODUCTION = {
    "voxity": "https://api.voxity.ai/mcp",
    "voxity-ims": "https://ims.voxity.ai/mcp",
}


def install(root, local):
    development = json.loads((root / "environments/development.json").read_text())
    if set(development) != set(PRODUCTION):
        raise ValueError("development.json must configure voxity and voxity-ims")
    for url in development.values():
        if not re.fullmatch(r"https://[a-z0-9-]+\.dev\.voxity\.ai/mcp", url):
            raise ValueError(f"Invalid development MCP URL: {url}")
    # Prepare every package before changing installed copies.
    with tempfile.TemporaryDirectory(prefix="voxity-dev-install-") as temporary:
        staged = Path(temporary)
        for name in PRODUCTION:
            dev_name = name + "-dev"
            package = staged / dev_name
            shutil.copytree(root / "plugins" / name, package)
            for relative in ("plugin.json", ".cursor-plugin/plugin.json", "mcp.json"):
                path = package / relative
                doc = json.loads(path.read_text())
                if relative == "mcp.json":
                    expected = {name: {"type": "streamable-http", "url": PRODUCTION[name]}}
                    if doc.get("mcpServers") != expected:
                        raise ValueError(f"Source must contain production MCP configuration: {path}")
                    doc["mcpServers"] = {dev_name: {
                        "type": "streamable-http", "url": development[name],
                    }}
                else:
                    doc["name"] = dev_name
                    doc["description"] = "DEV — " + doc.get("description", name)
                    if "displayName" in doc:
                        doc["displayName"] += " DEV"
                path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
        local.mkdir(parents=True, exist_ok=True)
        backup = None
        for name in PRODUCTION:
            dev_name = name + "-dev"
            target = local / dev_name
            if target.exists() or target.is_symlink():
                if backup is None:
                    backups = local.parent / "backups"
                    backups.mkdir(exist_ok=True)
                    backup = Path(tempfile.mkdtemp(prefix="voxity-dev-", dir=backups))
                target.rename(backup / dev_name)
            shutil.copytree(staged / dev_name, target)
            print(f"Installed {target}")
            print(json.loads((target / "mcp.json").read_text())["mcpServers"][dev_name]["url"])
        if backup:
            print(f"Previous DEV copies saved in {backup}")
    print("Reload Cursor to load the local DEV plugins.")


if __name__ == "__main__":
    install(ROOT, Path.home() / ".cursor/plugins/local")
