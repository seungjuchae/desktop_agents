# agents/tools/application_tool.py

import os
import time
import psutil
import pyautogui
import ctypes
from ctypes import wintypes
from agents.tools.base import BaseTool

user32 = ctypes.windll.user32

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
            self._open_app(app_name)

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

    def _open_app(self, name: str, delay: float = 1.0):
        """
        Try os.startfile first; if that fails, fall back to Start‑menu search.
        """
        print(f"🚀 Opening app: {name}")
        try:
            os.startfile(name)
            return
        except Exception:
            # fallback: Win key → type → Enter
            pyautogui.press("winleft")
            time.sleep(delay)
            pyautogui.write(name)
            time.sleep(delay)
            pyautogui.press("enter")

    def _kill_app(self, name: str):
        print(f"❌ Terminating app(s) matching: {name}")
        for proc in psutil.process_iter(attrs=["name", "pid"]):
            try:
                pname = proc.info["name"] or ""
                if name.lower() in pname.lower():
                    psutil.Process(proc.info["pid"]).terminate()
                    print(f"🛑 Terminated PID {proc.info['pid']} ({pname})")
            except Exception as e:
                print(f"⚠️ Failed to kill {pname}: {e}")

    def _is_running(self, name: str) -> bool:
        for proc in psutil.process_iter(attrs=["name"]):
            pname = proc.info["name"] or ""
            if name.lower() in pname.lower():
                return True
        return False

    def _focus_app(self, name: str, timeout: float = 5.0):
        """
        Enumerate windows; bring the first whose title matches `name` to front.
        """
        print(f"🎯 Focusing app window matching: {name}")

        EnumWindowsProc = ctypes.WINFUNCTYPE(
            wintypes.BOOL, wintypes.HWND, wintypes.LPARAM
        )

        found = False
        def _enum(hwnd, lParam):
            nonlocal found
            length = user32.GetWindowTextLengthW(hwnd)
            if length > 0 and not found:
                buf = ctypes.create_unicode_buffer(length + 1)
                user32.GetWindowTextW(hwnd, buf, length + 1)
                title = buf.value
                if name.lower() in title.lower():
                    user32.SetForegroundWindow(hwnd)
                    print(f"✅ Focused window: {title}")
                    found = True
                    return False  # stop enumeration
            return True

        user32.EnumWindows(EnumWindowsProc(_enum), 0)
        if not found:
            print(f"❌ No window found matching: {name}")

    def _list_apps(self):
        names = set()
        for proc in psutil.process_iter(attrs=["name"]):
            try:
                pname = proc.info["name"]
                if pname:
                    names.add(pname)
            except Exception:
                continue
        return sorted(names)
