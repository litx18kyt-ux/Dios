from playwright.sync_api import sync_playwright
import time, json

CBO_USER = "6958BANWARI"
CBO_PASS = "6958"
LOGIN_URL = "https://dios.myreporting.net/erp/login"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
    page = browser.new_page()

    print("[1] Logging in...")
    page.goto(LOGIN_URL, timeout=60000, wait_until="domcontentloaded")
    page.wait_for_timeout(1500)
    page.fill("input[type='text']:visible", CBO_USER)
    page.fill("input[type='password']:visible", CBO_PASS)
    page.keyboard.press("Enter")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(4000)

    print("Current URL:", page.url)
    print(f"Total Frames: {len(page.frames)}")

    for idx, f in enumerate(page.frames):
        print(f"\n--- Checking Frame {idx}: '{f.name}' ({f.url}) ---")
        menu_items = f.evaluate('''() => {
            const allLinks = Array.from(document.querySelectorAll('a, button, span, li, div'));
            return allLinks
                .filter(el => el.innerText && el.innerText.trim().length > 0 && el.innerText.trim().length < 40)
                .map(el => ({
                    tag: el.tagName,
                    text: el.innerText.trim(),
                    id: el.id,
                    className: el.className,
                    href: el.getAttribute('href')
                }))
                .filter(item => item.text.match(/(Report|DCR|Date Wise|Call Detail|Sales|Master)/i));
        }''')
        for item in menu_items[:15]:
            print(" ", item)

    browser.close()
