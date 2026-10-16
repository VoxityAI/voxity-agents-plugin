---
name: add-skill
description: Adds a skill to this Agent Plugin by creating skills/<id>/SKILL.md as an immediate child of skills/. Use when adding a skill to the voxity plugin or when creating a new SKILL.md under skills/.
---

# Add a skill

Create `skills/<SkillId>/SKILL.md` as an immediate child of `skills/` in the voxity package. In this repository that path is `plugins/voxity/skills/<SkillId>/SKILL.md`. Do not nest skill directories.

SkillId is lowercase kebab-case, 1 to 64 characters. It must not have a leading hyphen, a trailing hyphen, or consecutive hyphens.

The frontmatter `name` must equal the skill directory name.

Do not edit `plugin.json` or `mcp.json`.

Run `./validate.sh` from the repository root.

Clients discover skills as immediate children of `skills/`. Follow [Skills](https://agent-plugins.org/plugin-authors/skills) and the [Agent Skills specification](https://agentskills.io/specification).
