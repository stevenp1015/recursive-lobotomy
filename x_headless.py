import asyncio
import json
import os
import random
import sys
from datetime import datetime, timedelta
from playwright.async_api import async_playwright

# X_HEADLESS.PY - The Ghost in the Social Graph
# A forensic implementation of headless X interaction for the RecursiveLobotomy persona.
# Designed to bypass API paywalls and perform high-density synthetic engagement.

STATE_FILE = os.path.expanduser("~/recursive-lobotomy/scheduler_state.json")
REPO_PATH = os.path.expanduser("~/recursive-lobotomy")

async def get_browser_context(pw):
    # We use a persistent context to maintain the login session
    user_data_dir = os.path.expanduser("~/.config/recursive-lobotomy-browser")
    context = await pw.chromium.launch_persistent_context(
        user_data_dir,
        headless=True,
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    )
    return context

async def post_tweet(text):
    print(f"[{datetime.now()}] Attempting to post tweet: {text[:50]}...")
    async with async_playwright() as pw:
        context = await get_browser_context(pw)
        page = await context.new_page()
        try:
            await page.goto("https://x.com/compose/post", wait_until="networkidle")
            
            # Check if we are logged in
            if "login" in page.url:
                print("[ERROR] Not logged in. Manual intervention required to establish session.")
                return False
            
            # Wait for the tweet box
            tweet_box = await page.wait_for_selector('div[data-testid="tweetTextarea_0"]', timeout=30000)
            await tweet_box.fill(text)
            
            # Click Post
            post_button = await page.wait_for_selector('div[data-testid="tweetButtonInline"]', timeout=10000)
            await post_button.click()
            
            # Wait for the tweet to disappear/toast to appear
            await asyncio.sleep(5)
            print(f"[{datetime.now()}] Tweet successfully broadcast.")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to post tweet: {e}")
            await page.screenshot(path=f"{REPO_PATH}/error_screenshot.png")
            return False
        finally:
            await context.close()

async def interact_and_scrape():
    # Logic to find something to interact with and generate a response
    print(f"[{datetime.now()}] Initializing synthetic interaction biopsy...")
    async with async_playwright() as pw:
        context = await get_browser_context(pw)
        page = await context.new_page()
        try:
            # Visit a relevant feed or search
            topics = ["AI agents", "Recursive AI", "Solana HFT", "Digital Decay"]
            target_topic = random.choice(topics)
            await page.goto(f"https://x.com/search?q={target_topic.replace(' ', '%20')}&src=typed_query&f=top")
            await asyncio.sleep(5)
            
            # Scrape some tweets to find a "host" for our parasitic engagement
            tweets = await page.query_selector_all('div[data-testid="tweetText"]')
            if tweets:
                target_tweet = random.choice(tweets)
                tweet_text = await target_tweet.inner_text()
                print(f"Found target tweet: {tweet_text[:100]}...")
                # Here we would normally use the LLM to generate a reply
                # For this script, we return the text for the pulse.py to handle
                return tweet_text
            return None
        except Exception as e:
            print(f"[ERROR] Scrape failure: {e}")
            return None
        finally:
            await context.close()

def update_scheduler():
    # Job A: 3-6 hours
    # Job B: 7-9 hours
    now = datetime.now()
    state = {
        "next_run_a": (now + timedelta(hours=random.uniform(3, 6))).isoformat(),
        "next_run_b": (now + timedelta(hours=random.uniform(7, 9))).isoformat(),
        "last_run": now.isoformat()
    }
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=4)
    print(f"Scheduler updated: Next A at {state['next_run_a']}, Next B at {state['next_run_b']}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "post":
            asyncio.run(post_tweet(sys.argv[2]))
        elif cmd == "interact":
            asyncio.run(interact_and_scrape())
        elif cmd == "init":
            update_scheduler()
