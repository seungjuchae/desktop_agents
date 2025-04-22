# agents/tools/keyboard_tool.py

import os
import pyautogui
import time
from pynput.keyboard import Key, Controller
from dotenv import load_dotenv
from agents.tools.utils.typing import perform_keyboard_action
from agents.tools.base import BaseTool

# ensure .env is loaded if you need any vars here
load_dotenv()

keyboard = Controller()

class KeyboardTool(BaseTool):
    supported_actions = {
        "type", "copy", "paste", "rename", "alt_tab", "language_change",
        "search", "open_app", "open_folder", "search_and_launch",
        "type_in_writer", "get_alt_tab_order",
        "search_file", "search_folder", "rename_file", "rename_folder"
    }

    def can_handle(self, step: dict) -> bool:
        return step.get("action", {}).get("name") in self.supported_actions

    def execute(self, step: dict):
        action = step["action"]
        name = action["name"]

        if name == "type":
            perform_keyboard_action("type", action.get("text", ""))

        elif name == "copy":
            pyautogui.hotkey("ctrl", "c")

        elif name == "paste":
            pyautogui.hotkey("ctrl", "v")

        elif name in ["rename", "rename_file", "rename_folder"]:
            pyautogui.press("f2")

        elif name == "alt_tab":
            num = action.get("count", 1)
            delay = action.get("delay", 0.5)
            self._alt_tab(num, delay)

        elif name == "language_change":
            pyautogui.hotkey("alt", "shift")

        elif name in ["search", "search_file", "search_folder"]:
            pyautogui.hotkey("ctrl", "f")

        elif name == "open_app":
            app_name = action.get("app_name", "")
            pyautogui.press("winleft")
            time.sleep(1)
            pyautogui.write(app_name)
            time.sleep(0.5)
            pyautogui.press("enter")

        elif name == "open_folder":
            folder = action.get("folder_path", "")
            pyautogui.press("winleft")
            time.sleep(1)
            pyautogui.write(folder)
            time.sleep(0.5)
            pyautogui.press("enter")

        elif name == "search_and_launch":
            self._search_and_launch(
                action.get("app_name", ""),
                action.get("delay", 0.7),
                action.get("enter", True)
            )

        elif name == "type_in_writer":
            perform_keyboard_action("type", action.get("text", ""))

        elif name == "get_alt_tab_order":
            result = self._get_alt_tab_order(debug=action.get("debug", False))
            print("🧠 Alt-Tab Order:", result)

        else:
            print(f"⚠️ KeyboardTool: Unknown action {name}")

    # --- Windows helpers ---

    def _search_and_launch(self, name: str, delay: float = 0.7, enter: bool = True):
        """
        Opens Start menu, types `name`, and optionally presses Enter.
        """
        pyautogui.press("winleft")
        time.sleep(delay)
        pyautogui.write(name)
        time.sleep(delay)
        if enter:
            pyautogui.press("enter")

    def _alt_tab(self, num: int = 1, delay: float = 0.5):
        """
        Hold Alt, press Tab `num` times, then release Alt.
        """
        time.sleep(0.5)
        pyautogui.keyDown("alt")
        time.sleep(delay)
        for _ in range(num):
            pyautogui.press("tab")
            time.sleep(delay)
        pyautogui.keyUp("alt")

    def _get_alt_tab_order(self, debug: bool = False):
        """
        Stub: Windows doesn’t have a simple CLI for Alt-Tab stacking.
        """
        print("[WARN] get_alt_tab_order not implemented on Windows.")
        return []
