"""Test local DEV installation without touching the user's Cursor plugins."""

import importlib.util
import contextlib
import io
import json
from pathlib import Path
import shutil
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("installer", ROOT / "scripts/install-local-development.py")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "source"
        for name in ("plugins", "environments"):
            shutil.copytree(ROOT / name, self.root / name)
        self.local = Path(self.temporary.name) / "cursor/plugins/local"
        self.output = io.StringIO()
        self.redirect = contextlib.redirect_stdout(self.output)
        self.redirect.__enter__()
        self.addCleanup(self.redirect.__exit__, None, None, None)

    def snapshot(self, root):
        return {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()}

    def test_copies_dev_manifests_mcp_and_skills_without_changing_source(self):
        before = self.snapshot(self.root)
        installer.install(self.root, self.local)
        urls = json.loads((self.root / "environments/development.json").read_text())
        for name, production_url in installer.PRODUCTION.items():
            source = self.root / "plugins" / name
            package = self.local / (name + "-dev")
            self.assertTrue(package.is_dir())
            self.assertFalse(package.is_symlink())
            for relative in ("plugin.json", ".cursor-plugin/plugin.json"):
                original = json.loads((source / relative).read_text())
                self.assertNotIn("DEV", original["description"])
                copied = json.loads((package / relative).read_text())
                self.assertEqual(copied["name"], name + "-dev")
                self.assertTrue(copied["description"].startswith("DEV — "))
                self.assertEqual(original["author"], copied["author"])
                self.assertEqual(original["version"], copied["version"])
                if "displayName" in original:
                    self.assertEqual(original["displayName"] + " DEV", copied["displayName"])
            mcp = json.loads((package / "mcp.json").read_text())
            self.assertEqual(mcp["mcpServers"], {name + "-dev": {
                "type": "streamable-http", "url": urls[name],
            }})
            self.assertIn(production_url, (source / "mcp.json").read_text())
            for path in source.rglob("*"):
                if path.is_file() and path.name not in ("plugin.json", "mcp.json"):
                    self.assertEqual(path.read_bytes(), (package / path.relative_to(source)).read_bytes())
        self.assertEqual(before, self.snapshot(self.root))

    def test_reinstall_refreshes_skills_removes_stale_files_and_backs_up(self):
        installer.install(self.root, self.local)
        marker = self.local / "voxity-dev/obsolete"
        marker.write_text("previous install")
        skill = self.root / "plugins/voxity/skills/add-skill/SKILL.md"
        skill.write_text(skill.read_text() + "\nNew skill content.\n")
        # An unrelated plugin must survive refresh.
        other = self.local / "other-plugin"
        other.mkdir()
        (other / "keep").write_text("keep")
        installer.install(self.root, self.local)
        self.assertFalse(marker.exists())
        self.assertEqual(skill.read_bytes(), (self.local / "voxity-dev/skills/add-skill/SKILL.md").read_bytes())
        self.assertEqual("keep", (other / "keep").read_text())
        backups = list((self.local.parent / "backups").glob("*/voxity-dev/obsolete"))
        self.assertEqual(len(backups), 1)

    def test_invalid_source_preserves_existing_install(self):
        installer.install(self.root, self.local)
        before = self.snapshot(self.local)
        file = self.root / "plugins/voxity-ims/mcp.json"
        file.write_text(file.read_text().replace("ims.voxity.ai", "ims.dev.voxity.ai"))
        with self.assertRaises(ValueError):
            installer.install(self.root, self.local)
        self.assertEqual(before, self.snapshot(self.local))

    def test_replaces_dev_symlink_without_changing_its_target(self):
        self.local.mkdir(parents=True)
        source = self.root / "plugins/voxity"
        before = self.snapshot(source)
        (self.local / "voxity-dev").symlink_to(source, target_is_directory=True)
        installer.install(self.root, self.local)
        self.assertFalse((self.local / "voxity-dev").is_symlink())
        self.assertEqual(before, self.snapshot(source))
        backups = list((self.local.parent / "backups").glob("*/voxity-dev"))
        self.assertEqual(len(backups), 1)
        self.assertTrue(backups[0].is_symlink())

    def test_invalid_profile_leaves_install_untouched(self):
        installer.install(self.root, self.local)
        before = self.snapshot(self.local)
        file = self.root / "environments/development.json"
        config = json.loads(file.read_text())
        config["voxity"] = "https://api.voxity.ai/mcp"
        file.write_text(json.dumps(config))
        with self.assertRaises(ValueError):
            installer.install(self.root, self.local)
        self.assertEqual(before, self.snapshot(self.local))


if __name__ == "__main__":
    unittest.main()
