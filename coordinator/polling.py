# coordinator/polling.py

import os
import requests
import time
from platform import system

from coordinator.dispatch.ubuntu_dispatch import dispatch_to_agent as dispatch_ubuntu
from coordinator.dispatch.windows_dispatch import dispatch_to_agent as dispatch_windows



from dotenv import load_dotenv

load_dotenv()  

SERVER   = os.getenv("SERVER")
AGENT_ID = os.getenv("AGENT_ID")
API_KEY  = os.getenv("API_KEY")


PLATFORM = system().lower()

if PLATFORM == "linux":
    dispatch_to_agent = dispatch_ubuntu
elif PLATFORM == "windows":
    dispatch_to_agent = dispatch_windows
else:
    raise NotImplementedError(f"Unsupported OS: {PLATFORM}")

STEP_INTERVAL_SECONDS = 2

HEADERS = {
    "authorization": f"Bearer {API_KEY}",
    "content-type": "application/json"
}

def long_poll_and_execute():
    while True:
        try:
            print("🔁 Polling for command...")

            response = requests.get(
                f"{SERVER}/api/agents/{AGENT_ID}/wait_for_command",
                headers=HEADERS,
                timeout=60
            )
            response.raise_for_status()
            data = response.json()

            if command := data.get("command"):
                print("📥 Command received:")
                print(command)

                steps = command.get("steps", [])
                if not steps:
                    print("⚠️ No steps in command!")
                    continue

                plan_id = command.get("plan_id")
                print(f"📝 Plan ID: {plan_id}")

                for step in steps:
                    print(f"🚀 Executing step {step.get('step')}: {step.get('description')}")
                    dispatch_to_agent(step, plan_id=plan_id)
                    time.sleep(STEP_INTERVAL_SECONDS)

                # Report success
                requests.post(
                    f"{SERVER}/api/agents/{AGENT_ID}/report_result",
                    json={"result": {"status": "completed"}, "command_id": command.get("id")},
                    headers=HEADERS
                )

            time.sleep(1)

        except Exception as e:
            print(f"⚠️ Error during long-polling: {e}")
            time.sleep(5)


# Todo
# Optionally: send result back if needed
# (depends on what handle_command returns tho)
# e.g requests.post(...)