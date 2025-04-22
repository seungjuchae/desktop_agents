# coordinator/dispatch/windows_dispatch.py

from agents.windows.plan_executor_agent import PlanExecutorAgent
from agents.windows.browser_agent import BrowserAgent
from agents.windows.cli_agent import CLIAgent

AGENT_POOL = [
    BrowserAgent(),
    CLIAgent(),
    PlanExecutorAgent(),  # fallback
]

def dispatch_to_agent(step: dict, plan_id=None):
    action = step.get("action", {})
    action_name = action.get("name", "")
    print(f"\n🚀 [Windows] Dispatching action: {action_name}")

    for agent in AGENT_POOL:
        if agent.can_handle(step):
            print(f"✅ {agent.__class__.__name__} will handle: {action_name}")
            # 🔧 Pass plan_id to PlanExecutorAgent only
            if isinstance(agent, PlanExecutorAgent):
                return agent.execute(step, plan_id=plan_id)
            else:
                return agent.execute(step)

    print(f"⚠️ No Windows agent could handle: {action_name}")
