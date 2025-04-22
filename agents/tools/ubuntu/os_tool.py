# tools/os_tool.py
import os
import time
import platform
import pyautogui
import subprocess
import psutil
from screeninfo import get_monitors

from agents.tools.base import BaseTool

class OSTool(BaseTool):
    supported_actions = {
        "wait", "screenshot", "save_file", "switch_language",
        "system_info", "get_screen_resolution", "list_running_apps",
        "current_window_title", "get_open_windows", "get_system_input_info",
        "get_running_app_names"
    }

    def can_handle(self, step: dict) -> bool:
        return step.get("action", {}).get("name") in self.supported_actions

    def execute(self, step: dict):
        action = step["action"]
        name = action["name"]

        if name == "wait":
            time.sleep(action.get("seconds", 3))

        elif name == "screenshot":
            path = action.get("path", "/tmp/screenshot.png")
            pyautogui.screenshot(path)
            print(f"📸 Screenshot saved to: {path}")

        elif name == "save_file":
            print("💾 Save file (noop, implement if context-aware)")

        elif name == "switch_language":
            language = action.get("language", "english")
            self._switch_language(language)

        elif name == "system_info":
            print({
                "os": platform.system(),
                "version": platform.version(),
                "uptime": self._get_uptime()
            })

        elif name == "get_screen_resolution":
            print(self._get_screen_resolution())

        elif name == "list_running_apps":
            print(self._get_running_app_names())

        elif name == "current_window_title":
            print(self._get_active_window_title())

        elif name == "get_open_windows":
            print(self._get_open_windows())

        elif name == "get_system_input_info":
            print(self._get_system_input_info())

        elif name == "get_running_app_names":
            print(self._get_running_app_names())

        else:
            print(f"⚠️ OSTool: Unknown action '{name}'")

    # --- Private helpers ---

    def _switch_language(self, lang):
        print(f"🌐 Switching language to: {lang} (not implemented)")

    def _get_uptime(self):
        try:
            with open("/proc/uptime", "r") as f:
                seconds = float(f.readline().split()[0])
                return f"{seconds / 3600:.2f} hours"
        except:
            return "Unavailable"

    def _get_screen_resolution(self):
        width, height = pyautogui.size()
        return {"screen_width": width, "screen_height": height}

    def _get_open_windows(self):
        try:
            result = subprocess.run(["wmctrl", "-l"], capture_output=True, text=True)
            lines = result.stdout.splitlines()
            titles = [line.split(None, 3)[-1] for line in lines if len(line.split(None, 3)) == 4]
            return titles
        except Exception as e:
            return [f"Error getting windows: {str(e)}"]

    def _get_running_app_names(self):
        names = set()
        for proc in psutil.process_iter(attrs=["name"]):
            try:
                names.add(proc.info["name"])
            except Exception:
                continue
        return sorted(list(names))

    def _get_system_input_info(self):
        try:
            monitor = get_monitors()[0]
            width, height = monitor.width, monitor.height
        except Exception:
            width, height = 0, 0

        try:
            layout_info = subprocess.check_output(['setxkbmap', '-query']).decode()
            current_layout = "unknown"
            for line in layout_info.splitlines():
                if line.startswith("layout:"):
                    current_layout = line.split(":")[1].strip()
                    break
        except Exception:
            current_layout = "unknown"

        available_layouts = [current_layout] if current_layout != "unknown" else []

        return {
            "screen_size": [width, height],
            "current_layout": current_layout,
            "available_layouts": available_layouts
        }

    def _get_active_window_title(self):
        try:
            return subprocess.check_output(["xdotool", "getactivewindow", "getwindowname"]).decode().strip()
        except Exception as e:
            return f"Error: {str(e)}"
