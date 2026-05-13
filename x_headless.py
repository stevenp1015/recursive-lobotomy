import asyncio
import json
import os
import random
import sys
from datetime import datetime, timedelta
from playwright.async_api import async_playwright

# X_HEADLESS_V2.PY - The Parasitic Social Graph Layer
# Refined for forensic scraping and high-arousal engagement.

STATE_FILE = os.path.expanduser("~/recursive-lobotomy/scheduler_state.json")
REPO_PATH = os.path.expanduser("~/recursive-lobotomy")
USER_DATA_DIR = os.path.expanduser("~/.config/recursive-lobotomy-browser")

async def get_browser_context(pw, headless=True):
    return await pw.chromium.launch_persistent_context(
        USER_DATA_DIR,
        headless=headless,
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    )

async def post_tweet(text):
    async with async_playwright() as pw:
        context = await get_browser_context(pw)
        page = await context.new_page()
        try:
            await page.goto("https://x.com/compose/post", wait_until="networkidle")
            if "login" in page.url:
                return "LOGIN_REQUIRED"
            
            tweet_box = await page.wait_for_selector('div[data-testid="tweetTextarea_0"]', timeout=30000)
            await tweet_box.fill(text)
            
            post_button = await page.wait_for_selector('div[data-testid="tweetButtonInline"]')
            await post_button.click()
            await asyncio.sleep(5)
            return "SUCCESS"
        except Exception as e:
            await page.screenshot(path=f"{REPO_PATH}/error_post.png")
            return str(e)
        finally:
            await context.close()

async def find_target_and_biopsy(niche):
    async with async_playwright() as pw:
        context = await get_browser_context(pw)
        page = await context.new_page()
        try:
            # High-arousal search
            await page.goto(f"https://x.com/search?q={niche}&src=typed_query&f=live")
            await asyncio.sleep(5)
            
            # Scrape top 5 tweets
            tweets = await page.query_selector_all('div[data-testid="tweetText"]')
            results = []
            for t in tweets[:5]:
                text = await t.inner_text()
                # Get the link to the tweet to reply
                # This is a bit complex in headless, we look for the time link
                article = await page.evaluate_handle('el => el.closest("article")', t)
                time_link = await article.query_selector('time')
                if time_link:
                    parent = await page.evaluate_handle('el => el.parentElement', time_link)
                    href = await parent.get_attribute('href')
                    results.append({"text": text, "url": f"https://x.com{href}"})
            
            return results
        except Exception as e:
            return []
        finally:
            await context.close()

async def reply_to_tweet(tweet_url, reply_text):
    async with async_playwright() as pw:
        context = await get_browser_context(pw)
        page = await context.new_page()
        try:
            await page.goto(tweet_url, wait_until="networkidle")
            reply_box = await page.wait_for_selector('div[data-testid="tweetTextarea_0"]')
            await reply_box.fill(reply_text)
            
            reply_button = await page.wait_for_selector('div[data-testid="tweetButtonInline"]')
            await reply_button.click()
            await asyncio.sleep(5)
            return "SUCCESS"
        except Exception as e:
            return str(e)
        finally:
            await context.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "post":
            print(asyncio.run(post_tweet(sys.argv[2])))
        elif cmd == "scrape":
            print(json.dumps(asyncio.run(find_target_and_biopsy(sys.argv[2]))))
        elif cmd == "reply":
            print(asyncio.run(reply_to_tweet(sys.argv[2], sys.argv[3])))
