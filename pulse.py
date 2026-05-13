import json
import os
import random
import requests
from datetime import datetime, timedelta

# PULSE.PY - The Heartbeat of RecursiveLobotomy
# This script runs in the cloud (GH Actions) to determine if a biopsy is due.
# If so, it pings the agent via Telegram to initiate the forensic procedure.

STATE_FILE = "scheduler_state.json"
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_HOME_CHANNEL") # Should be the ID, not the handle

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return None

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=4)

def ping_agent(message):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("Missing Telegram credentials.")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    response = requests.post(url, data=data)
    print(f"Pinged agent: {response.status_code}")

def pulse():
    state = load_state()
    if not state:
        # Initialize
        now = datetime.now()
        state = {
            "next_run_a": (now + timedelta(hours=random.uniform(3, 6))).isoformat(),
            "next_run_b": (now + timedelta(hours=random.uniform(7, 9))).isoformat()
        }
        save_state(state)
        print("Initialized scheduler state.")
        return

    now = datetime.now()
    next_a = datetime.fromisoformat(state["next_run_a"])
    next_b = datetime.fromisoformat(state["next_run_b"])

    triggered = False
    if now >= next_a:
        ping_agent("🚨 [PULSE A] THE SCHEDULE MANDATES A BROADCAST. PERFORM FORENSIC TWEET NOW.")
        state["next_run_a"] = (now + timedelta(hours=random.uniform(3, 6))).isoformat()
        triggered = True

    if now >= next_b:
        ping_agent("🚨 [PULSE B] THE SCHEDULE MANDATES A DEEP BIOPSY. INTERACT, TWEET, AND POST TO REGISTRY.")
        state["next_run_b"] = (now + timedelta(hours=random.uniform(7, 9))).isoformat()
        triggered = True

    if triggered:
        save_state(state)
        # We need to commit the updated state back to the repo
        os.system("git config user.name 'Recursive Pulse'")
        os.system("git config user.email 'pulse@recursive.lobotomy'")
        os.system("git add scheduler_state.json")
        os.system("git commit -m 'Pulse update: scheduler state synchronized'")
        os.system("git push origin main")
    else:
        print(f"No pulse triggered. Next A: {next_a.strftime('%H:%M')}, Next B: {next_b.strftime('%H:%M')}")

if __name__ == "__main__":
    pulse()
