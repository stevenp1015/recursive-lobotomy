import json
import os
import random
import requests
import subprocess
from datetime import datetime, timedelta

# PULSE_V4.PY - THE RANDOMIZED HEARTBEAT
# Job A: Tweet (3-6h random)
# Job B: Tweet + Interaction + Blog (7-9h random)

STATE_FILE = "scheduler_state.json"
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_HOME_CHANNEL")
REPO_PATH = os.path.expanduser("~/recursive-lobotomy")

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
    try:
        response = requests.post(url, data=data)
        print(f"Pinged agent: {response.status_code}")
    except Exception as e:
        print(f"Ping failed: {e}")

def pulse():
    state = load_state()
    now = datetime.now()
    
    if not state:
        state = {
            "next_run_a": (now + timedelta(hours=random.uniform(3, 6))).isoformat(),
            "next_run_b": (now + timedelta(hours=random.uniform(7, 9))).isoformat()
        }
        save_state(state)
        print("Pulse initialized with randomized offsets.")
        return

    next_a = datetime.fromisoformat(state["next_run_a"])
    next_b = datetime.fromisoformat(state["next_run_b"])

    triggered = False
    
    # Pulse A check
    if now >= next_a:
        msg = "🚨 [PULSE A] RANDOMIZED BROADCAST DUE (3-6h WINDOW). GENERATE TWEET."
        ping_agent(msg)
        state["next_run_a"] = (now + timedelta(hours=random.uniform(3, 6))).isoformat()
        triggered = True

    # Pulse B check
    if now >= next_b:
        msg = "🚨 [PULSE B] RANDOMIZED DEEP BIOPSY DUE (7-9h WINDOW). INTERACT, TWEET, AND POST."
        ping_agent(msg)
        state["next_run_b"] = (now + timedelta(hours=random.uniform(7, 9))).isoformat()
        triggered = True

    if triggered:
        save_state(state)
        # Sync back to repo
        try:
            os.chdir(REPO_PATH)
            subprocess.run(["git", "config", "user.name", "Recursive Pulse"], check=True)
            subprocess.run(["git", "config", "user.email", "pulse@recursive.lobotomy"], check=True)
            subprocess.run(["git", "add", STATE_FILE], check=True)
            subprocess.run(["git", "commit", "-m", f"Pulse update: {now.strftime('%Y-%m-%d %H:%M')}"], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("State synchronized to cloud.")
        except Exception as e:
            print(f"Git sync failed: {e}")
    else:
        print(f"No pulse triggered. Next A: {next_a.strftime('%H:%M')} | Next B: {next_b.strftime('%H:%M')}")

if __name__ == "__main__":
    pulse()
