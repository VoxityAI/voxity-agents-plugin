# Install Voxity plugins in Cursor

This repository is a Cursor marketplace that contains Agent Plugins 1.0.0 packages, including `voxity` and `voxity-ims`. Each package declares a remote Voxity MCP server. Cursor is the MCP client and the OAuth client. Read [Build an Agent Plugin](https://agent-plugins.org/plugin-authors/build-an-agent-plugin) for the portable package format. The source is [VoxityAI/agent-plugins](https://github.com/VoxityAI/agent-plugins).

## Add from this folder

1. Open **Customize**, then **Plugins**.
2. Choose **+ Add**.
3. Select this repository root, the folder that contains `.cursor-plugin/marketplace.json`.
4. Install **voxity** and **voxity-ims**.

That flow reads the marketplace manifest. A root-only `plugin.json` is not enough.

## Test a development copy in Cursor

Files in this repository always use production URLs and descriptions. To install
separate DEV copies in Cursor, run from the repository root (Python 3.9+ required):

```bash
python3 scripts/install-local-development.py
```

The script copies the packages as real directories to:

- `~/.cursor/plugins/local/voxity-dev`
- `~/.cursor/plugins/local/voxity-ims-dev`

Only the installed copies are changed: plugin and MCP server names get `-dev`,
display names and descriptions include `DEV`, and the MCP URLs become
`https://api.dev.voxity.ai/mcp` and `https://ims.dev.voxity.ai/mcp`.
Development URLs are configured in `environments/development.json`.

Reload Cursor, confirm **Voxity DEV** and **Voxity IMS DEV** in Customize, and
complete development MCP sign-in. Use the Command Palette's **Developer: Reload
Window** command to reload. Under MCP connections, confirm the URLs above before
running tools. Disable production MCP connections during
DEV testing to avoid selecting the wrong environment. This local install is for
Cursor; Grok Bot does not load these copies in our tested setup.

Edit source files and skills only in this repository, then rerun the same command
and reload Cursor to refresh the installed copies. Reinstalling replaces stale
DEV files and saves previous copies under `~/.cursor/plugins/backups/`.
Other local plugins are left alone. The source packages, Git configuration, and
staged files are never modified by the script.

The local copies have distinct names so a marketplace-installed production plugin
does not override them. Use real copies: Cursor rejects symlinks pointing outside
its local plugins directory. If they do not appear after reload, check that local
plugin imports are allowed by your team's policy.

To stop local testing, disable the DEV plugins in Customize. To uninstall only
these development copies:

```bash
rm -r ~/.cursor/plugins/local/voxity-dev ~/.cursor/plugins/local/voxity-ims-dev
```

Reload Cursor after uninstalling. Production plugins and the source checkout are
unaffected. This workflow needs no Git filters, hooks, or generated marketplace.

## Connect

Do not copy this package into an app repo. Install the plugin at user scope. A project-scope install in this marketplace repo does not appear in other windows.

1. Install **voxity** and **voxity-ims** with **Add from this folder**.
2. Open the app in Cursor. Open **Customize** and confirm the plugins are listed.
3. When Cursor prompts for Voxity MCP authorization, complete that sign-in. Do not run a plugin CLI. Do not paste a token. Do not start a local redirect server.
4. Use Voxity through the plugin MCP tools.

The source packages use `https://api.voxity.ai/mcp` and `https://ims.voxity.ai/mcp`. The local DEV copies use the corresponding `*.dev.voxity.ai` endpoints. Authentication follows the MCP authorization spec. Cursor owns the redirect. If that host is missing `/mcp` or does not advertise protected-resource metadata, Cursor disables only the MCP entry. Skills still load.

A previous `~/.voxity` session file is unused. You can delete it.

## Add a skill

Create `plugins/voxity/skills/<id>/SKILL.md`. Invoke the `add-skill` skill if you want the agent to write it. Do not edit `plugin.json` or `mcp.json`.

## Prove the package

Run `./validate.sh` from the repository root to validate the production packages. Run `python3 scripts/test-install-local-development.py` to verify DEV installation, source preservation, and refresh behavior in a scratch directory.
