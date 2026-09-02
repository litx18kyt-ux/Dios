from playwright.sync_api import sync_playwright
import time

CBO_USER = "6958BANWARI"
CBO_PASS = "6958"
LOGIN_URL = "https://dios.myreporting.net/erp/login"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
    context = browser.new_context(viewport={'width': 1440, 'height': 900})
    page = context.new_page()

    print("[1] Logging in...")
    page.goto(LOGIN_URL, timeout=60000, wait_until="domcontentloaded")
    page.wait_for_timeout(1500)
    page.fill("input[type='text']:visible", CBO_USER)
    page.fill("input[type='password']:visible", CBO_PASS)
    page.keyboard.press("Enter")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)

    print("[2] Clicking Reports menu...")
    page.locator("text='Reports'").first.click()
    page.wait_for_timeout(1000)

    print("[3] Hovering DCR Reports...")
    page.locator("text='DCR Reports'").first.hover()
    page.wait_for_timeout(1000)

    print("[4] Clicking Date Wise Call Detail...")
    page.locator("text='Date Wise Call Detail'").first.click()
    page.wait_for_timeout(3000)

    print("\n[5] Current URL / Modal State:")
    print("Page URL:", page.url)

    # Inspect all inputs and buttons on screen
    form_elements = page.evaluate('''() => {
        const inputs = Array.from(document.querySelectorAll('input, select, button'));
        return inputs.filter(el => el.offsetParent !== null).map(el => ({
            tag: el.tagName,
            id: el.id,
            name: el.name,
            placeholder: el.placeholder,
            value: el.value,
            text: el.innerText
        }));
    }''')
    for el in form_elements:
        print(" ", el)

    page.screenshot(path='/workspaces/Dios/csv_output/dcr_modal_open.png')
    print("\n📸 Screenshot saved: csv_output/dcr_modal_open.png")
    browser.close()
