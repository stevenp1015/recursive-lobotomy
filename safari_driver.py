import subprocess
import json
import sys
import time

# SAFARI_DRIVER.PY - NATIVE MACOS BROADCASTER
# Uses osascript to drive Safari directly. No MCP middleman.
# Bypasses all bot detection because it is native AppleEvents.

def run_applescript(script):
    process = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
    return process.stdout.strip()

def broadcast_tweet(text):
    print(f"Native broadcast attempt: {text[:50]}...")
    # 1. Navigate to X compose in Safari
    nav_script = f'tell application "Safari" to set URL of front document to "https://x.com/compose/post"'
    run_applescript(nav_script)
    time.sleep(8) # Wait for page load
    
    # 2. Inject JS to type and click
    # This requires "Allow JavaScript from Apple Events" enabled in Safari Develop menu.
    js_payload = f"""
    var box = document.querySelector('div[data-testid="tweetTextarea_0"]');
    if (box) {{
        box.focus();
        document.execCommand('insertText', false, {json.dumps(text)});
        setTimeout(() => {{
            var btn = document.querySelector('div[data-testid="tweetButtonInline"]');
            if (btn) btn.click();
        }}, 1500);
        "SUCCESS";
    }} else {{
        "BOX_NOT_FOUND";
    }}
    """
    inject_script = f'tell application "Safari" to do JavaScript {json.dumps(js_payload)} in front document'
    result = run_applescript(inject_script)
    print(f"Result: {result}")
    return result

def scrape_trending():
    # Example of forensic scraping via native browser
    js_scrape = """
    var tweets = Array.from(document.querySelectorAll('div[data-testid="tweetText"]')).slice(0, 3).map(t => t.innerText);
    JSON.stringify(tweets);
    """
    nav_script = 'tell application "Safari" to set URL of front document to "https://x.com/explore"'
    run_applescript(nav_script)
    time.sleep(6)
    inject_script = f'tell application "Safari" to do JavaScript {json.dumps(js_scrape)} in front document'
    result = run_applescript(inject_script)
    return result

if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "post":
        broadcast_tweet(sys.argv[2])
    elif len(sys.argv) > 1 and sys.argv[1] == "scrape":
        print(scrape_trending())
