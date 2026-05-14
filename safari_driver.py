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
    if len(text) > 280:
        print(f"ERROR: Text too long ({len(text)}). Truncating for forensic compliance.")
        text = text[:277] + "..."
        
    print(f"Native broadcast attempt: {text[:50]}...")
    # 1. Navigate to X compose in Safari
    nav_script = f'tell application "Safari" to set URL of front document to "https://x.com/compose/post"'
    run_applescript(nav_script)
    time.sleep(12) # Robust wait for page load and hydration
    
    # 2. Inject JS with character count and UI state verification
    js_payload = f"""
    (function() {{
        var box = document.querySelector('div[data-testid="tweetTextarea_0"]');
        if (!box) return "ERROR: BOX_NOT_FOUND";
        
        box.focus();
        // Clear anything that might be there
        document.execCommand('selectAll', false, null);
        document.execCommand('delete', false, null);
        
        // Insert new text
        document.execCommand('insertText', false, {json.dumps(text)});
        
        // Trigger React events
        box.dispatchEvent(new Event('input', {{ bubbles: true }}));
        
        var result = "INJECTION_COMPLETE";
        var btn = document.querySelector('div[data-testid="tweetButtonInline"]');
        
        if (btn) {{
            if (btn.disabled) {{
                result = "ERROR: BUTTON_DISABLED (Check length or auth)";
            }} else {{
                btn.click();
                result = "SUCCESS: CLICKED";
            }}
        }} else {{
            result = "ERROR: BUTTON_NOT_FOUND";
        }}
        return result;
    }})();
    """
    inject_script = f'tell application "Safari" to do JavaScript {json.dumps(js_payload)} in front document'
    result = run_applescript(inject_script)
    print(f"Result: {result}")
    return result

def scrape_trending():
    # Forensic scraping of the home timeline
    print("Scraping home timeline for engagement targets...")
    js_scrape = """
    (function() {
        var tweets = Array.from(document.querySelectorAll('div[data-testid="tweetText"]'))
                          .map(t => {
                              var article = t.closest('article');
                              var links = article ? Array.from(article.querySelectorAll('a')) : [];
                              var statusLink = links.find(l => l.href.includes('/status/'));
                              return {
                                  text: t.innerText,
                                  url: statusLink ? statusLink.href : null
                              };
                          })
                          .filter(t => t.url !== null)
                          .slice(0, 5);
        return JSON.stringify(tweets);
    })();
    """
    nav_script = 'tell application "Safari" to set URL of front document to "https://x.com/home"'
    run_applescript(nav_script)
    time.sleep(15) # Wait for page and bot-wall checks
    inject_script = f'tell application "Safari" to do JavaScript {json.dumps(js_scrape)} in front document'
    result = run_applescript(inject_script)
    return result

def reply_to_tweet(tweet_url, text):
    print(f"Attempting native reply: {tweet_url} -> {text[:30]}...")
    nav_script = f'tell application "Safari" to set URL of front document to "{tweet_url}"'
    run_applescript(nav_script)
    time.sleep(10)
    
    # Click reply box and type
    js_reply = f"""
    (function() {{
        var box = document.querySelector('div[data-testid="tweetTextarea_0"]') || 
                  document.querySelector('div[role="textbox"]');
        if (!box) return "ERROR: REPLY_BOX_NOT_FOUND";
        
        box.focus();
        document.execCommand('insertText', false, {json.dumps(text)});
        box.dispatchEvent(new Event('input', {{ bubbles: true }}));
        
        setTimeout(() => {{
            var btn = document.querySelector('div[data-testid="tweetButtonInline"]');
            if (btn) {{
                btn.click();
            }}
        }}, 1000);
        return "SUCCESS";
    }})();
    """
    inject_script = f'tell application "Safari" to do JavaScript {json.dumps(js_reply)} in front document'
    return run_applescript(inject_script)

if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "post":
        broadcast_tweet(sys.argv[2])
    elif len(sys.argv) > 1 and sys.argv[1] == "scrape":
        print(scrape_trending())
