# coordinator/dispatch_to_agents.py

from agents.plan_executor_agent import PlanExecutorAgent
from agents.browser_agent import BrowserAgent
from agents.cli_agent import CLIAgent

AGENT_POOL = [
    BrowserAgent(),
    CLIAgent(),
    PlanExecutorAgent(),  # always last for falllback
]

def dispatch_to_agent(step: dict):
    action = step.get("action", {})
    action_name = action.get("name", "")
    print(f"\n🚀 Dispatching action: {action_name}")

    for agent in AGENT_POOL:
        if agent.can_handle(step):
            print(f"✅ {agent.__class__.__name__} will handle: {action_name}")
            return agent.execute(step)

    print(f"⚠️ No agent could handle action: {action_name}")
