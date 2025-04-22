# agents/tools/os_tool.py

import os
import time
import platform
import pyautogui
import psutil
import ctypes
from ctypes import wintypes
from screeninfo import get_monitors

from agents.tools.base import BaseTool

user32 = ctypes.windll.user32

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
            path = action.get("path", os.path.join(os.getcwd(), "screenshot.png"))
            pyautogui.screenshot(path)
            print(f"📸 Screenshot saved to: {path}")

        elif name == "save_file":
            print("💾 Save file (noop, implement if context-aware)")

        elif name == "switch_language":
            # Windows: typically Alt+Shift or Win+Space
            pyautogui.hotkey("alt", "shift")

        elif name == "system_info":
            info = {
                "os": platform.system(),
                "version": platform.version(),
                "uptime_hours": f"{self._get_uptime():.2f}"
            }
            print(info)

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

    def _get_uptime(self) -> float:
        """Return uptime in hours."""
        boot = psutil.boot_time()
        return (time.time() - boot) / 3600

    def _get_screen_resolution(self):
        monitors = get_monitors()
        if monitors:
            m = monitors[0]
            return {"screen_width": m.width, "screen_height": m.height}
        else:
            w, h = pyautogui.size()
            return {"screen_width": w, "screen_height": h}

    def _get_running_app_names(self):
        names = set()
        for proc in psutil.process_iter(attrs=["name"]):
            try:
                names.add(proc.info["name"])
            except Exception:
                continue
        return sorted(names)

    def _get_system_input_info(self):
        # screen size
        size = self._get_screen_resolution()
        # current keyboard layout via Win32
        try:
            hkl = user32.GetKeyboardLayout(0)
            lid = hkl & 0xFFFF
            current = hex(lid)
        except Exception:
            current = "unknown"
        return {
            "screen_size": [size["screen_width"], size["screen_height"]],
            "current_layout": current,
            "available_layouts": [current] if current != "unknown" else []
        }

    def _get_active_window_title(self) -> str:
        try:
            hwnd = user32.GetForegroundWindow()
            length = user32.GetWindowTextLengthW(hwnd)
            buf = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buf, length + 1)
            return buf.value
        except Exception as e:
            return f"Error: {e}"

    def _get_open_windows(self):
        titles = []

        # callback for EnumWindows
        EnumWindowsProc = ctypes.WINFUNCTYPE(
            wintypes.BOOL, wintypes.HWND, wintypes.LPARAM
        )
        def _enum_windows(hwnd, lParam):
            length = user32.GetWindowTextLengthW(hwnd)
            if length > 0:
                buf = ctypes.create_unicode_buffer(length + 1)
                user32.GetWindowTextW(hwnd, buf, length + 1)
                title = buf.value.strip()
                if title:
                    titles.append(title)
            return True

        user32.EnumWindows(EnumWindowsProc(_enum_windows), 0)
        return titles
