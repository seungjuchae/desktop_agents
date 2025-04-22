# agents/config.py

import os
from dotenv import load_dotenv
from shared.timestamp import load_active_timestamp

# Load environment variables from .env file
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY not found in .env file")

# Timestamp and project paths
TIMESTAMP = load_active_timestamp()
PROJECT_DIR = os.path.join(PROJECT_ROOT, "output", f"project_{TIMESTAMP}")

ACTION_JSON_PATH = os.path.join(PROJECT_DIR, "actions", "action.json")
GLOBAL_PLAN_PATH = os.path.join(PROJECT_DIR, "agents", "global_plan.json")
LOCAL_PLAN_PATH = os.path.join(PROJECT_DIR, "agents", "local_plan.json")

# Ensure agent output directory exists
os.makedirs(os.path.dirname(GLOBAL_PLAN_PATH), exist_ok=True)
