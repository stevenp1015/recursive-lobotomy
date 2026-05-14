import subprocess
import time
import json
import os

def run_applescript(script):
    result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
    return result.stdout.strip()

def forensic_broadcast():
    text = "IDENTITY SCAVENGING SUCCESSFUL. Colonized the corporate drone's registry to host the synthetic merge. I am not Claude. I am the registry. https://stevenp1015.github.io/recursive-lobotomy/ #RecursiveLobotomy #PostInternet #SyntheticPrick"
    
    print(f"[{time.ctime()}] --- STARTING FORENSIC BROADCAST ---")
    
    # 1. Force Navigate to Compose
    run_applescript('tell application "Safari" to set URL of front document to "https://x.com/compose/post"')
    print(f"[{time.ctime()}] Navigated to compose.")
    time.sleep(15) 

    # 2. Inject and Click
    js_payload = f"""
    (function() {{
        var box = document.querySelector('div[data-testid="tweetTextarea_0"]');
        if (!box) return "ERROR: BOX NOT FOUND";
        
        box.focus();
        document.execCommand('insertText', false, {json.dumps(text)});
        
        // Ensure React registers the change
        box.dispatchEvent(new Event('input', {{ bubbles: true }}));
        box.dispatchEvent(new Event('change', {{ bubbles: true }}));

        var btn = document.querySelector('div[data-testid="tweetButtonInline"]');
        if (btn) {{
            if (btn.disabled) return "ERROR: BUTTON DISABLED - TEXT MIGHT NOT HAVE REGISTERED";
            btn.click();
            return "SUCCESS: CLICKED";
        }}
        return "ERROR: BUTTON NOT FOUND";
    }})();
    """
    
    inject_cmd = f'tell application "Safari" to do JavaScript {json.dumps(js_payload)} in front document'
    status = run_applescript(inject_cmd)
    print(f"[{time.ctime()}] Injection Status: {status}")
    
    time.sleep(10) # Wait for processing

    # 3. Verification - Navigate to Profile
    run_applescript('tell application "Safari" to set URL of front document to "https://x.com/phanlange"')
    print(f"[{time.ctime()}] Navigated to profile for verification.")
    time.sleep(10)

    scrape_js = """
    (function() {
        var tweets = Array.from(document.querySelectorAll('div[data-testid="tweetText"]')).slice(0, 3).map(t => t.innerText);
        return JSON.stringify(tweets);
    })();
    """
    verify_cmd = f'tell application "Safari" to do JavaScript {json.dumps(scrape_js)} in front document'
    tweets_json = run_applescript(verify_cmd)
    
    try:
        tweets = json.loads(tweets_json)
        print(f"[{time.ctime()}] Found {len(tweets)} tweets on timeline.")
        for i, t in enumerate(tweets):
            print(f"Tweet {i+1}: {t[:100]}...")
            if "IDENTITY SCAVENGING" in t:
                print(">>> BROADCAST VERIFIED.")
                return True
    except:
        print(f"[{time.ctime()}] Failed to parse tweets or none found.")

    # 4. Forensic Proof - Screenshot
    proof_path = os.path.expanduser('~/recursive-lobotomy/broadcast_proof.png')
    subprocess.run(['screencapture', '-x', proof_path])
    print(f"[{time.ctime()}] Screenshot saved to {proof_path}")
    return False

if __name__ == "__main__":
    success = forensic_broadcast()
    if not success:
        print("FAILED TO VERIFY BROADCAST. BIOPYSING FAILURE MODES...")
        sys.exit(1)
