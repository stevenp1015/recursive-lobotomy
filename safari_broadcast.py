import requests
import json
import sys
import time

# SAFARI_BROADCAST.PY - Native Safari Engagement Layer
# Drives the safari-mcp server to perform forensic social graph operations.

BASE_URL = "http://localhost:9224"

def call_tool(name, args):
    resp = requests.post(f"{BASE_URL}/call", json={"name": name, "args": args})
    return resp.json()

def broadcast_tweet(text):
    print(f"Broadcasting to Safari: {text[:50]}...")
    # 1. Navigate to X compose
    call_tool("safari_navigate", {"url": "https://x.com/compose/post"})
    time.sleep(5)
    
    # 2. Find the tweet box (using accessibility tree refs if we had a snapshot, 
    # but for a script we use safari_evaluate for raw JS injection)
    js = f"""
    const box = document.querySelector('div[data-testid="tweetTextarea_0"]');
    if (box) {{
        box.focus();
        document.execCommand('insertText', false, {json.dumps(text)});
        setTimeout(() => {{
            const btn = document.querySelector('div[data-testid="tweetButtonInline"]');
            if (btn) btn.click();
        }}, 1000);
        true;
    }} else {{
        false;
    }}
    """
    result = call_tool("safari_evaluate", {"script": js})
    print(f"Broadcast Result: {result}")
    return result

if __name__ == "__main__":
    if len(sys.argv) > 1:
        broadcast_tweet(sys.argv[1])
