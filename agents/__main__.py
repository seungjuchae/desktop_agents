# agents/__main__.py

import json
from agents.filesystem import FileSystemAgent
from agents.browser import BrowserAgent
from agents.os import OSAgent
from agents.apps import ApplicationAgent
from actions.config import LOCAL_PLAN_PATH

AGENTS = [
    FileSystemAgent(),
    BrowserAgent(),
    OSAgent(),
    ApplicationAgent()
]

def load_plan():
    with open(LOCAL_PLAN_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    plan = load_plan()
    print("🤖 Executing local plan...\n")

    for step in plan:
        handled = False
        for agent in AGENTS:
            if agent.can_handle(step):
                print(f"[→] {agent} handling: {step['description']}")
                agent.execute(step)
                handled = True
                break

        if not handled:
            print(f"[⚠️] No agent could handle: {step['description']}")

if __name__ == "__main__":
    main()

