# tools/application_tool.py

import subprocess
import time
import psutil
from agents.tools.base import BaseTool

class ApplicationTool(BaseTool):
    supported_actions = {
        "open_app", "close_app",
        "is_app_running", "focus_app",
        "list_apps"
    }

    def can_handle(self, step: dict) -> bool:
        return step.get("action", {}).get("name") in self.supported_actions

    def execute(self, step: dict):
        action = step["action"]
        name = action["name"]

        if name == "open_app":
            app_name = action.get("app_name", "")
            self._search_and_launch(app_name)

        elif name == "close_app":
            app_name = action.get("app_name", "")
            self._kill_app(app_name)

        elif name == "is_app_running":
            app_name = action.get("app_name", "")
            running = self._is_running(app_name)
            print(f"🟢 App '{app_name}' running: {running}")

        elif name == "focus_app":
            app_name = action.get("app_name", "")
            self._focus_app(app_name)

        elif name == "list_apps":
            apps = self._list_apps()
            print("🚀 Running apps:", apps)

        else:
            print(f"⚠️ ApplicationTool: Unknown action '{name}'")

    # --- Internal methods ---

    def _search_and_launch(self, name: str, delay: float = 0.7):
        print(f"🚀 Launching app: {name}")
        subprocess.run(["xdotool", "key", "Super_L"])
        time.sleep(delay)
        subprocess.run(["xdotool", "type", name])
        time.sleep(2)
        subprocess.run(["xdotool", "key", "Return"])

    def _kill_app(self, name: str):
        print(f"❌ Trying to kill: {name}")
        for proc in psutil.process_iter(attrs=["name", "pid"]):
            try:
                if name.lower() in proc.info["name"].lower():
                    psutil.Process(proc.info["pid"]).terminate()
                    print(f"🛑 Terminated PID {proc.info['pid']}")
            except Exception as e:
                print(f"⚠️ Failed to kill {proc}: {e}")

    def _is_running(self, name: str) -> bool:
        for proc in psutil.process_iter(attrs=["name"]):
            if name.lower() in proc.info["name"].lower():
                return True
        return False

    def _focus_app(self, name: str):
        print(f"🎯 Trying to focus app: {name}")
        try:
            output = subprocess.check_output(["wmctrl", "-lx"]).decode()
            for line in output.splitlines():
                if name.lower() in line.lower():
                    win_id = line.split()[0]
                    subprocess.run(["wmctrl", "-i", "-a", win_id])
                    print(f"✅ Focused window: {win_id}")
                    return
            print(f"❌ No window found for app: {name}")
        except Exception as e:
            print(f"⚠️ Focus error: {e}")

    def _list_apps(self):
        names = set()
        for proc in psutil.process_iter(attrs=["name"]):
            try:
                names.add(proc.info["name"])
            except:
                continue
        return sorted(list(names))

