from playwright.sync_api import sync_playwright
import time

CBO_USER = "6958BANWARI"
CBO_PASS = "6958"
LOGIN_URL = "https://dios.myreporting.net/erp/login"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
    context = browser.new_context(viewport={'width': 1440, 'height': 900}, accept_downloads=True)
    page = context.new_page()

    print("[1] Logging in to CBO...")
    page.goto(LOGIN_URL, timeout=60000, wait_until="domcontentloaded")
    page.wait_for_timeout(1500)
    page.fill("input[type='text']:visible", CBO_USER)
    page.fill("input[type='password']:visible", CBO_PASS)
    
    login_btn = page.locator("button:visible:has-text('Login'), input[type='submit']:visible, .btn-success:visible").first
    if login_btn.count() > 0:
        login_btn.click()
    else:
        page.keyboard.press("Enter")

    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3500)
    print("Logged in! Current URL:", page.url)

    print("\n[2] Opening Reports -> DCR Reports -> Date Wise Call Detail...")
    # Click Reports
    page.locator("a:has-text('Reports'), span:has-text('Reports')").first.click()
    page.wait_for_timeout(1000)

    # Click DCR Reports
    page.locator("a:has-text('DCR Reports'), span:has-text('DCR Reports'), td:has-text('DCR Reports')").first.hover()
    page.wait_for_timeout(1000)

    # Click Date Wise Call Detail
    page.locator("text='Date Wise Call Detail'").first.click()
    page.wait_for_timeout(3000)

    # Check open modal or iframe
    print("\n[3] Checking Modal & Iframes...")
    for idx, f in enumerate(page.frames):
        print(f"Frame {idx}: '{f.name}' -> URL: {f.url}")
        
    page.screenshot(path='/workspaces/Dios/csv_output/dcr_modal_success.png')
    print("\n📸 Modal screenshot saved to: csv_output/dcr_modal_success.png")

    browser.close()
