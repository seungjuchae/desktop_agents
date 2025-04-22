# agents/browser_agent.py
from agents.base import BaseAgent
from agents.tools.windows.keyboard_tool import KeyboardTool
from agents.tools.windows.mouse_tool import MouseTool
import pyautogui
import time

from agents.tools.utils.focus import wait_and_focus

class BrowserAgent(BaseAgent):
    def __init__(self):
        self.keyboard = KeyboardTool()
        self.mouse = MouseTool()

        self.supported_actions = {
            "open_browser", "new_tab", "close_tab", "search_web",
            "go_to_url", "scroll_down", "scroll_up",
            "next_tab", "prev_tab", "click_element"
        }

    def can_handle(self, step: dict) -> bool:
        return step.get("action", {}).get("name") in self.supported_actions

    def execute(self, step: dict):
        action = step["action"]
        name = action["name"]

        if name == "open_browser":
            app = action.get("app_name", "chrome")
            self.keyboard.execute({"action": {"name": "open_app", "app_name": app}})
            time.sleep(2)
            # wait_and_focus(app, timeout=10)

        elif name == "new_tab":
            pyautogui.hotkey("ctrl", "t")

        elif name == "close_tab":
            pyautogui.hotkey("ctrl", "w")

        elif name == "search_web":
            app = action.get("app_name", "chrome")  # todo: default to chrome but change later
            # wait_and_focus(app, timeout=5)  # 

            query = action.get("query", "")
            pyautogui.hotkey("ctrl", "l")
            time.sleep(0.2)
            pyautogui.write(query)
            pyautogui.press("enter")

        elif name == "go_to_url":
            app = action.get("app_name", "chrome")
            # wait_and_focus(app, timeout=5)

            url = action.get("url", "")
            pyautogui.hotkey("ctrl", "l")
            time.sleep(0.2)
            pyautogui.write(url)
            pyautogui.press("enter")

        elif name == "scroll_down":
            pyautogui.scroll(-500)

        elif name == "scroll_up":
            pyautogui.scroll(500)

        elif name == "next_tab":
            pyautogui.hotkey("ctrl", "tab")

        elif name == "prev_tab":
            pyautogui.hotkey("ctrl", "shift", "tab")

        elif name == "click_element":
            x = action.get("x", 0)
            y = action.get("y", 0)
            pyautogui.click(x, y)

        else:
            print(f"⚠️ BrowserAgent: Unknown action '{name}'")
