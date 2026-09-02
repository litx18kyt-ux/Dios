from playwright.sync_api import sync_playwright
import time, json

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
    page.keyboard.press("Enter")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)

    print("[2] Opening Date Wise Call Detail modal via Direct JS...")
    # Direct click on Date Wise Call Detail link
    clicked_menu = page.evaluate('''() => {
        const elms = Array.from(document.querySelectorAll('a, span, li, div'));
        const target = elms.find(e => e.innerText && e.innerText.trim() === 'Date Wise Call Detail');
        if (target) {
            target.click();
            return true;
        }
        return false;
    }''')
    print("Clicked Date Wise Call Detail:", clicked_menu)
    page.wait_for_timeout(3000)

    # Find the modal and inputs
    print("[3] Filling Date Range (01/08/2026 to 31/08/2026)...")
    inputs_found = page.evaluate('''() => {
        const inputs = Array.from(document.querySelectorAll('input:visible'));
        // Find date inputs
        const dateInputs = inputs.filter(i => i.value && i.value.includes('/'));
        if (dateInputs.length >= 2) {
            dateInputs[0].value = '01/08/2026';
            dateInputs[0].dispatchEvent(new Event('input', {bubbles: true}));
            dateInputs[0].dispatchEvent(new Event('change', {bubbles: true}));

            dateInputs[1].value = '31/08/2026';
            dateInputs[1].dispatchEvent(new Event('input', {bubbles: true}));
            dateInputs[1].dispatchEvent(new Event('change', {bubbles: true}));
            return { success: true, from: dateInputs[0].value, to: dateInputs[1].value };
        }
        return { success: false, total_inputs: inputs.length };
    }''')
    print("Date Input Result:", inputs_found)

    print("[4] Clicking GO button...")
    # Click GO
    page.evaluate('''() => {
        const btns = Array.from(document.querySelectorAll('button, input[type=button], input[type=submit]'));
        const goBtn = btns.find(b => (b.innerText || b.value || '').trim().toUpperCase().includes('GO'));
        if (goBtn) goBtn.click();
    }''')

    time.sleep(6)

    # Capture screenshot
    page.screenshot(path='/workspaces/Dios/csv_output/dcr_result.png')
    print("📸 Screenshot saved to: csv_output/dcr_result.png")

    # Scrape Table
    print("\n[5] Scraping DCR Progress Table...")
    for f in page.frames:
        table_rows = f.evaluate('''() => {
            const trs = Array.from(document.querySelectorAll('tr'));
            return trs.map(r => Array.from(r.querySelectorAll('td, th')).map(c => c.innerText.trim())).filter(r => r.length >= 3);
        }''')
        if len(table_rows) > 3:
            print(f"Found {len(table_rows)} rows in frame '{f.name}'!")
            for r in table_rows[:8]:
                print("  •", r)

    browser.close()
