# agents/cli_agent.py
from agents.base import BaseAgent
from agents.tools.windows.keyboard_tool import KeyboardTool

import time

class CLIAgent(BaseAgent):
    def __init__(self):
        self.keyboard = KeyboardTool()

        self.supported_actions = {
            "open_terminal", "new_terminal_tab", "close_terminal_tab",
            "type_command", "run_command", "clear_terminal"
        }

    def can_handle(self, step: dict) -> bool:
        return step.get("action", {}).get("name") in self.supported_actions

    def execute(self, step: dict):
        action = step["action"]
        name = action["name"]

        if name == "open_terminal":
            self.keyboard._alt_tab()  # Optional: bring desktop focus
            self._hotkey("ctrl", "alt", "t")
            time.sleep(1.5)

        elif name == "new_terminal_tab":
            self._hotkey("ctrl", "shift", "t")
            time.sleep(1)

        elif name == "close_terminal_tab":
            self._hotkey("ctrl", "shift", "w")

        elif name == "clear_terminal":
            self._type_and_enter("clear")

        elif name == "type_command":
            self._type(action.get("command", ""))

        elif name == "run_command":
            self._type_and_enter(action.get("command", ""))

        else:
            print(f"⚠️ CLIAgent: Unknown action {name}")

    # --- Internals ---

    def _hotkey(self, *keys):
        for k in keys:
            self.keyboard_press(k)
        for k in reversed(keys):
            self.keyboard_release(k)

    def keyboard_press(self, key):
        import pyautogui
        pyautogui.keyDown(key)

    def keyboard_release(self, key):
        import pyautogui
        pyautogui.keyUp(key)

    def _type(self, text):
        import pyautogui
        pyautogui.write(text, interval=0.03)

    def _type_and_enter(self, text):
        self._type(text)
        import pyautogui
        pyautogui.press("enter")
