# agents/plan_executor_agent.py

import os
import time
from pathlib import Path

from agents.base import BaseAgent

from agents.tools.windows.keyboard_tool      import KeyboardTool
from agents.tools.windows.mouse_tool         import MouseTool
from agents.tools.windows.os_tool            import OSTool
from agents.tools.windows.filesystem_tool    import FileSystemTool
from agents.tools.windows.application_tool   import ApplicationTool

from agents.tools.utils.screenshot import take_screenshot
from agents.tools.utils.upload     import upload_screenshot

# These can come from your .env loader instead of hard‑coding
AGENT_ID = os.getenv("AGENT_ID")
SERVER   = os.getenv("SERVER")
API_KEY  = os.getenv("API_KEY")


class PlanExecutorAgent(BaseAgent):
    def __init__(self):
        self.tools = [
            KeyboardTool(),
            MouseTool(),
            OSTool(),
            FileSystemTool(),
            ApplicationTool(),
        ]

    def can_handle(self, step: dict) -> bool:
        return any(tool.can_handle(step) for tool in self.tools)

    def execute(self, step: dict, plan_id=None):
        action     = step.get("action", {})
        action_name= action.get("name", "")
        step_num   = step.get("step", "unknown")

        # prepare temp paths
        base = Path(os.getcwd()) / "temp_screenshots"
        base.mkdir(exist_ok=True)
        before_path = base / f"before_step_{step_num}.png"
        after_path  = base / f"after_step_{step_num}.png"

        # 1) Screenshot BEFORE
        take_screenshot(str(before_path))
        upload_screenshot(
            agent_id   = AGENT_ID,
            plan_id    = plan_id,
            step       = step_num,
            stage      = "before",
            file_path  = str(before_path),
            server_url = SERVER,
            api_key    = API_KEY,
        )

        # 2) Optional focus logic (uncomment if you want)
        # app_name = action.get("app_name") or action.get("target_app")
        # if app_name and action_name not in ("focus_app","is_app_running"):
        #     wait_and_focus(app_name, timeout=10)

        time.sleep(2)  # give Windows a moment

        # 3) Execute the action
        for tool in self.tools:
            if tool.can_handle(step):
                print(f"🔧 {tool.__class__.__name__} will handle: {action_name}")
                tool.execute(step)
                break
        else:
            print(f"⚠️ PlanExecutorAgent: No tool could handle: {action_name}")

        time.sleep(1)  # allow UI to settle

        # 4) Screenshot AFTER
        take_screenshot(str(after_path))
        upload_screenshot(
            agent_id   = AGENT_ID,
            plan_id    = plan_id,
            step       = step_num,
            stage      = "after",
            file_path  = str(after_path),
            server_url = SERVER,
            api_key    = API_KEY,
        )
