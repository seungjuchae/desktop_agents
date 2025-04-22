# agents/tools/filesystem_tool.py
import os
import shutil
from pathlib import Path
from agents.tools.base import BaseTool

class FileSystemTool(BaseTool):
    supported_actions = {
        "create_folder", "delete_folder",
        "create_file", "delete_file",
        "move_file", "copy_file",
        "list_directory",
        "programmatic_rename_file", "programmatic_rename_folder"
    }

    def can_handle(self, step: dict) -> bool:
        return step.get("action", {}).get("name") in self.supported_actions

    def execute(self, step: dict):
        action = step["action"]
        name = action["name"]

        try:
            if name == "create_folder":
                folder = Path(action["path"]).expanduser()
                folder.mkdir(parents=True, exist_ok=True)
                print(f"📁 Created folder: {folder}")

            elif name == "delete_folder":
                folder = Path(action["path"]).expanduser()
                shutil.rmtree(folder)
                print(f"🗑️ Deleted folder: {folder}")

            elif name == "create_file":
                file = Path(action["path"]).expanduser()
                file.parent.mkdir(parents=True, exist_ok=True)
                file.write_text(action.get("content", ""))
                print(f"📄 Created file: {file}")

            elif name == "delete_file":
                file = Path(action["path"]).expanduser()
                file.unlink()
                print(f"🗑️ Deleted file: {file}")

            elif name == "move_file":
                src = Path(action["src"]).expanduser()
                dst = Path(action["dst"]).expanduser()
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(src), str(dst))
                print(f"📂 Moved file: {src} → {dst}")

            elif name == "copy_file":
                src = Path(action["src"]).expanduser()
                dst = Path(action["dst"]).expanduser()
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(str(src), str(dst))
                print(f"📋 Copied file: {src} → {dst}")

            elif name == "list_directory":
                directory = Path(action.get("path", ".")).expanduser()
                contents = [p.name for p in directory.iterdir()]
                print(f"📁 Contents of {directory}: {contents}")

            elif name in ["programmatic_rename_file", "programmatic_rename_folder"]:
                src = Path(action["src"]).expanduser()
                dst = Path(action["dst"]).expanduser()
                dst.parent.mkdir(parents=True, exist_ok=True)
                src.rename(dst)
                print(f"✏️ Renamed: {src} → {dst}")

            else:
                print(f"⚠️ FileSystemTool: Unknown action '{name}'")

        except Exception as e:
            print(f"❌ FileSystemTool error: {e}")
