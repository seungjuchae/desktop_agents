# agents/plan_executor_agent.py

import time

from agents.base import BaseAgent

from agents.tools.ubuntu.keyboard_tool import KeyboardTool
from agents.tools.ubuntu.mouse_tool import MouseTool
from agents.tools.ubuntu.os_tool import OSTool
from agents.tools.ubuntu.filesystem_tool import FileSystemTool
from agents.tools.ubuntu.application_tool import ApplicationTool
from agents.tools.utils.focus import wait_and_focus
from agents.tools.utils.screenshot import take_screenshot  # ✅ NEW
from agents.tools.utils.upload import upload_screenshot  # ✅ NEW
# from config import AGENT_ID, SERVER, API_KEY  # ✅ Assuming you already have these

# Optionally: send result back if needed
# (depends on what handle_command returns)
# requests.post(...)

# # Prod
# AGENT_ID = "bf1bdef4-7139-4f0f-a32c-69def4f28ff6"
# SERVER = "https://usedesktop.com"
# API_KEY = "NBgbj-w6bxnC3Mvh4eN5cubbWzUEkrIqNnuY06yF3ZY"

# # Dev
# AGENT_ID = "c52f8fef-82e9-4d68-8f31-979d76b416ae"
# SERVER = "https://dev.usedesktop.com"
# API_KEY = "ssCwi9jEq3tOt0kZg3r7btMZ5zAe9cciAqSQfsH7CgA"

# # Local
AGENT_ID = "f6e5cf52-10ec-4fd3-b305-9988429db2a6"
SERVER = "http://localhost:4000"
API_KEY = "NNc0BvBtOfoNj_U11Ka8ltuBWAPhfbBmMDOe9ZJdHUY"


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
        action = step.get("action", {})
        action_name = action.get("name", "")
        step_number = step.get("step", "unknown")

        # Screenshot BEFORE
        before_path = f"/tmp/before_step_{step_number}.png"
        take_screenshot(before_path)
        upload_screenshot(
            agent_id=AGENT_ID,
            plan_id=plan_id,
            step=step_number,
            stage="before",
            file_path=before_path,
            server_url=SERVER,
            api_key=API_KEY
        )

        # Focus if needed
        app_name = action.get("app_name") or action.get("target_app")
        # if app_name and action_name not in ["focus_app", "is_app_running"]:
        #     wait_and_focus(app_name, timeout=10)



        time.sleep(7)

        # Action execution
        for tool in self.tools:
            if tool.can_handle(step):
                print(f"🔧 {tool.__class__.__name__} will handle: {action_name}")
                tool.execute(step)
                break
        else:
            print(f"⚠️ PlanExecutorAgent: No tool could handle {action_name}")

        # Screenshot AFTER
        after_path = f"/tmp/after_step_{step_number}.png"
        take_screenshot(after_path)
        upload_screenshot(
            agent_id=AGENT_ID,
            plan_id=plan_id,
            step=step_number,
            stage="after",
            file_path=after_path,
            server_url=SERVER,
            api_key=API_KEY
        )
