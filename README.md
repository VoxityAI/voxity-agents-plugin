# Install Voxity plugins in Cursor

This repository is a Cursor marketplace that contains Agent Plugins 1.0.0 packages, including `voxity` and `voxity-ims`. Each package declares a remote Voxity MCP server. Cursor is the MCP client and the OAuth client. Read [Build an Agent Plugin](https://agent-plugins.org/plugin-authors/build-an-agent-plugin) for the portable package format. The source is [VoxityAI/agent-plugins](https://github.com/VoxityAI/agent-plugins).

## Add from this folder

1. Open **Customize**, then **Plugins**.
2. Choose **+ Add**.
3. Select this repository root, the folder that contains `.cursor-plugin/marketplace.json`.
4. Install **voxity** and **voxity-ims**.

That flow reads the marketplace manifest. A root-only `plugin.json` is not enough.

## Link for local development

The clone folder may be `agent-plugins`. Symlink the package directory, not the git root.

```bash
git clone git@github.com:VoxityAI/agent-plugins.git
cd agent-plugins
mkdir -p ~/.cursor/plugins/local
ln -sfn "$(pwd)/plugins/voxity" ~/.cursor/plugins/local/voxity
ln -sfn "$(pwd)/plugins/voxity-ims" ~/.cursor/plugins/local/voxity-ims
```

Reload Cursor. Confirm `voxity` and `voxity-ims` in Customize.

## Connect

Do not copy this package into an app repo. Install the plugin at user scope, or use the local symlink above. A project-scope install in this marketplace repo does not appear in other windows.

1. Install **voxity** and **voxity-ims** with **Add from this folder** or **Link for local development**.
2. Open the app in Cursor. Open **Customize** and confirm the plugins are listed.
3. When Cursor prompts for Voxity MCP authorization, complete that sign-in. Do not run a plugin CLI. Do not paste a token. Do not start a local redirect server.
4. Use Voxity through the plugin MCP tools.

`voxity` points Cursor at `https://api.voxity.ai/mcp`. `voxity-ims` points Cursor at `https://ims.voxity.ai/mcp`. Authentication follows the MCP authorization spec. Cursor owns the redirect. If that host is missing `/mcp` or does not advertise protected-resource metadata, Cursor disables only the MCP entry. Skills still load.

A previous `~/.voxity` session file is unused. You can delete it.

## Add a skill

Create `plugins/voxity/skills/<id>/SKILL.md`. Invoke the `add-skill` skill if you want the agent to write it. Do not edit `plugin.json` or `mcp.json`.

## Prove the package

Run `./validate.sh` from the repository root.
