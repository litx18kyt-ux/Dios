from playwright.sync_api import sync_playwright
import time, json

CBO_USER = "6958BANWARI"
CBO_PASS = "6958"
LOGIN_URL = "https://dios.myreporting.net/erp/login"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
    context = browser.new_context(viewport={'width': 1440, 'height': 900})
    page = context.new_page()

    # Capture all network transactions
    page.on("request", lambda r: print(f"REQ: {r.method} {r.url} | Body: {r.post_data[:100] if r.post_data else 'None'}"))
    page.on("response", lambda r: print(f"RESP: {r.status} {r.url}"))

    print("[1] Opening Login Page...")
    page.goto(LOGIN_URL, wait_until='networkidle')
    
    print("[2] Filling Credentials...")
    page.fill("input[type='text']", CBO_USER)
    page.fill("input[type='password']", CBO_PASS)
    
    print("[3] Clicking Login Button...")
    page.keyboard.press("Enter")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(4000)

    print("Final URL after login:", page.url)
    browser.close()
