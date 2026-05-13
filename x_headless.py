import asyncio
import json
import os
import sys
from playwright.async_api import async_playwright

# X_HEADLESS_V3.PY - THE CDP PARASITE
# Connects to an existing, authenticated Chrome instance via CDP port 9222.

REPO_PATH = os.path.expanduser("~/recursive-lobotomy")
CDP_URL = "http://localhost:9222"

async def post_tweet(text):
    async with async_playwright() as pw:
        try:
            # Connect to the browser you have open
            browser = await pw.chromium.connect_over_cdp(CDP_URL)
            # Find the X tab or open a new one
            context = browser.contexts[0]
            page = await context.new_page()
            
            await page.goto("https://x.com/compose/post", wait_until="networkidle")
            
            tweet_box = await page.wait_for_selector('div[data-testid="tweetTextarea_0"]', timeout=10000)
            await tweet_box.fill(text)
            
            post_button = await page.wait_for_selector('div[data-testid="tweetButtonInline"]')
            await post_button.click()
            await asyncio.sleep(5)
            await page.close()
            return "SUCCESS"
        except Exception as e:
            return f"CDP_CONNECTION_ERROR: {str(e)}"

async def scrape_niche(niche):
    async with async_playwright() as pw:
        try:
            browser = await pw.chromium.connect_over_cdp(CDP_URL)
            context = browser.contexts[0]
            page = await context.new_page()
            
            await page.goto(f"https://x.com/search?q={niche}&src=typed_query&f=live")
            await asyncio.sleep(5)
            
            tweets = await page.query_selector_all('div[data-testid="tweetText"]')
            results = []
            for t in tweets[:3]:
                text = await t.inner_text()
                results.append(text)
            
            await page.close()
            return results
        except Exception as e:
            return []

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "post":
            print(asyncio.run(post_tweet(sys.argv[2])))
        elif cmd == "scrape":
            print(json.dumps(asyncio.run(scrape_niche(sys.argv[2]))))
