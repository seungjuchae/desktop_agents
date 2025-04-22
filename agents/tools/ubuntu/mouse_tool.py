import time
import pyautogui
import math
import random

from agents.tools.base import BaseTool

class MouseTool(BaseTool):
    supported_actions = {
        "click", "left_click", "right_click", "double_click",
        "click_specific_area", "move", "drag"
    }

    def can_handle(self, step: dict) -> bool:
        return step.get("action", {}).get("name") in self.supported_actions

    def execute(self, step: dict):
        action = step["action"]
        name = action["name"]

        x = action.get("x", 500)
        y = action.get("y", 500)
        delay = action.get("delay", 0.2)

        if name in ["click", "left_click"]:
            self._perform_mouse_action(x, y, "left_click", delay)

        elif name == "right_click":
            self._perform_mouse_action(x, y, "right_click", delay)

        elif name == "double_click":
            self._perform_mouse_action(x, y, "double_click", delay)

        elif name == "click_specific_area":
            self._perform_mouse_action(x, y, "left_click", delay)

        elif name == "move":
            self._human_like_move(x, y, fast=True)

        elif name == "drag":
            x2 = action.get("x2", x + 200)
            y2 = action.get("y2", y + 100)
            self._drag(x, y, x2, y2)

        else:
            print(f"⚠️ MouseTool: Unknown action '{name}'")

    # --- Private helpers ---

    def _human_like_move(self, dest_x, dest_y, fast=True):
        start_x, start_y = pyautogui.position()
        distance = math.hypot(dest_x - start_x, dest_y - start_y)

        steps = max(2, int(distance / (50 if fast else 10)))

        for i in range(steps):
            t = i / steps
            cur_x = start_x + (dest_x - start_x) * t + random.uniform(-1, 1)
            cur_y = start_y + (dest_y - start_y) * t + random.uniform(-1, 1)
            pyautogui.moveTo(cur_x, cur_y, duration=0.001)

        pyautogui.moveTo(dest_x, dest_y, duration=0.001)

    def _perform_mouse_action(self, x, y, action_type="left_click", delay=0.0):
        if delay > 0:
            time.sleep(delay)

        self._human_like_move(x, y, fast=True)

        if action_type == "left_click":
            pyautogui.click()
        elif action_type == "right_click":
            pyautogui.rightClick()
        elif action_type == "double_click":
            pyautogui.doubleClick()

    def _drag(self, x1, y1, x2, y2):
        print(f"🖱️ Dragging from ({x1},{y1}) to ({x2},{y2})")
        self._human_like_move(x1, y1, fast=False)
        pyautogui.mouseDown()
        self._human_like_move(x2, y2, fast=False)
        pyautogui.mouseUp()
