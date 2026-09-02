from playwright.sync_api import sync_playwright
import time

CBO_USER = "6958BANWARI"
CBO_PASS = "6958"
LOGIN_URL = "https://dios.myreporting.net/erp/login"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
    context = browser.new_context(viewport={'width': 1440, 'height': 900}, accept_downloads=True)
    page = context.new_page()

    print("[1] Logging in...")
    page.goto(LOGIN_URL, timeout=60000, wait_until="domcontentloaded")
    page.wait_for_timeout(1500)
    page.fill("input[type='text']:visible", CBO_USER)
    page.fill("input[type='password']:visible", CBO_PASS)
    page.locator("button:visible:has-text('Login'), input[type='submit']:visible, .btn-success:visible").first.click()
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)

    print("[2] Searching and clicking 'Reports' -> 'DCR Reports' -> 'Date Wise Call Detail' via DOM...")
    clicked = page.evaluate('''() => {
        const allElements = Array.from(document.querySelectorAll('a, li, span, div'));
        
        // 1. Click Reports
        const reportsMenu = allElements.find(e => e.innerText && e.innerText.trim() === 'Reports');
        if (reportsMenu) reportsMenu.click();
        
        // 2. Find and click Date Wise Call Detail directly
        const dcrItem = allElements.find(e => e.innerText && e.innerText.trim().includes('Date Wise Call Detail'));
        if (dcrItem) {
            dcrItem.click();
            return { found: true, text: dcrItem.innerText };
        }
        return { found: false };
    }''')
    print("Click result:", clicked)
    page.wait_for_timeout(3000)

    # Let's check modal or dialogs
    print("\n[3] Checking visible modals/forms:")
    modals = page.evaluate('''() => {
        const dialogs = Array.from(document.querySelectorAll('.modal, .dialog, [role=\"dialog\"], iframe'));
        return dialogs.map(d => ({
            id: d.id,
            className: d.className,
            text: d.innerText ? d.innerText.substring(0, 100) : '',
            src: d.src || ''
        }));
    }''')
    for m in modals:
        print(" ", m)

    page.screenshot(path='/workspaces/Dios/csv_output/dcr_modal.png')
    print("\n📸 Screenshot saved to: csv_output/dcr_modal.png")
    browser.close()
