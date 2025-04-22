import os
import shutil

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
                path = action.get("path", "")
                os.makedirs(path, exist_ok=True)
                print(f"📁 Created folder: {path}")

            elif name == "delete_folder":
                path = action.get("path", "")
                shutil.rmtree(path)
                print(f"🗑️ Deleted folder: {path}")

            elif name == "create_file":
                path = action.get("path", "")
                content = action.get("content", "")
                with open(path, "w") as f:
                    f.write(content)
                print(f"📄 Created file: {path}")

            elif name == "delete_file":
                path = action.get("path", "")
                os.remove(path)
                print(f"🗑️ Deleted file: {path}")

            elif name == "move_file":
                src = action.get("src")
                dst = action.get("dst")
                shutil.move(src, dst)
                print(f"📂 Moved file: {src} → {dst}")

            elif name == "copy_file":
                src = action.get("src")
                dst = action.get("dst")
                shutil.copy(src, dst)
                print(f"📋 Copied file: {src} → {dst}")

            elif name == "list_directory":
                path = action.get("path", ".")
                files = os.listdir(path)
                print(f"📁 Contents of {path}: {files}")

            elif name in ["programmatic_rename_file", "programmatic_rename_folder"]:
                src = action.get("src")
                dst = action.get("dst")
                os.rename(src, dst)
                print(f"✏️ Renamed: {src} → {dst}")

            else:
                print(f"⚠️ FileSystemTool: Unknown action '{name}'")

        except Exception as e:
            print(f"❌ FileSystemTool error: {e}")
