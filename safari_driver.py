import subprocess
import json
import sys
import time

# SAFARI_DRIVER.PY - NATIVE MACOS BROADCASTER V3 (HYPER-ROBUST)
# Uses osascript and System Events for hardware-level automation.
# Bypasses React hydration and DOM timing issues by using keystrokes.

def run_applescript(script):
    process = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
    if process.returncode != 0:
        print(f"DEBUG: AppleScript error: {process.stderr.strip()}")
    return process.stdout.strip()

def broadcast_tweet(text):
    if len(text) > 280:
        print(f"WARNING: Text too long ({len(text)}). Truncating.")
        text = text[:277] + "..."
        
    print(f"Native broadcast sequence initiated...")
    
    # 0. Ensure Safari is active and focused
    run_applescript('tell application "Safari" to activate')
    time.sleep(1)
    
    # 1. Open the compose window
    run_applescript('tell application "Safari" to set URL of front document to "https://x.com/compose/post"')
    
    # 2. Wait for the page to be ready for keystrokes
    print("Waiting for compose window to hydrate...")
    time.sleep(10) 
    
    # 3. Use System Events to keystroke the text (robust for React)
    # We escape the text for AppleScript strings
    escaped_text = text.replace('"', '\\"').replace('\n', '\\r')
    keystroke_script = f"""
    tell application "System Events"
        tell process "Safari"
            # Ensure we are focused on the text area
            # We use a small delay to make sure the nav is settled
            delay 2
            keystroke "{escaped_text}"
            delay 1
            # Cmd + Enter to post
            keystroke return using command down
        end tell
    end tell
    """
    run_applescript(keystroke_script)
    print("Keystrokes injected. Sent Cmd+Enter.")
    
    # 4. Verification loop
    return verify_post()

def verify_post():
    print("Verifying signal propagation...")
    for i in range(10):
        time.sleep(3)
        current_url = run_applescript('tell application "Safari" to get URL of front document')
        print(f"[{i+1}/10] Current URL: {current_url}")
        
        # If we are back at home or a status page, it worked
        if "x.com/home" in current_url or "/status/" in current_url:
            print("SUCCESS: Signal is in the graph.")
            return "SUCCESS"
        
        # If we are still at compose, it failed or is slow
        if "compose/post" not in current_url:
            print("SUCCESS: Redirect detected.")
            return "SUCCESS"
            
    print("ERROR: Verification timeout. Signal status unknown.")
    return "TIMEOUT"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Support positional text for backward compatibility or explicit 'post'
        if sys.argv[1] == "post" and len(sys.argv) > 2:
            broadcast_tweet(sys.argv[2])
        else:
            broadcast_tweet(sys.argv[1])
    else:
        print("Usage: python3 safari_driver.py post 'Text' or python3 safari_driver.py 'Text'")
