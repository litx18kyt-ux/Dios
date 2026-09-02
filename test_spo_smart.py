from playwright.sync_api import sync_playwright
import time, json

CBO_USER = "6958BANWARI"
CBO_PASS = "6958"
LOGIN_URL = "https://dios.myreporting.net/erp/login"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
    context = browser.new_context(viewport={'width': 1440, 'height': 900}, accept_downloads=True)
    page = context.new_page()
    page.on('dialog', lambda d: d.accept())

    print("[1] Logging in to CBO...")
    page.goto(LOGIN_URL, timeout=60000, wait_until="domcontentloaded")
    page.wait_for_timeout(1500)
    page.fill("input[type='text']:visible", CBO_USER)
    page.fill("input[type='password']:visible", CBO_PASS)
    page.locator("button:visible:has-text('Login'), input[type='submit']:visible, .btn-success:visible").first.click()
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)

    print("[2] Opening 'Sales & Targets' menu...")
    page.locator("a:has-text('Reports'), span:has-text('Reports')").first.click()
    page.wait_for_timeout(800)

    # Hover over Sales & Targets
    page.evaluate('''() => {
        const elms = Array.from(document.querySelectorAll('a, span, li, td'));
        const st = elms.find(e => (e.innerText || '').trim() === 'Sales & Targets');
        if (st) {
            st.dispatchEvent(new MouseEvent('mouseover', {bubbles: true}));
            st.click();
        }
    }''')
    page.wait_for_timeout(1000)

    # List all submenu items under Sales & Targets
    menu_items = page.evaluate('''() => {
        const elms = Array.from(document.querySelectorAll('a, span, li'));
        return elms.filter(e => (e.innerText || '').includes('SPO')).map(e => ({
            text: e.innerText.trim(),
            tag: e.tagName,
            id: e.id,
            className: e.className
        }));
    }''')
    print("Found SPO Menu Items:", menu_items)

    # Click on the exact SPO Stockist Wise
    print("\n[3] Clicking 'SPO Stockist Wise'...")
    page.evaluate('''() => {
        const elms = Array.from(document.querySelectorAll('a, span, li'));
        const target = elms.find(e => (e.innerText || '').trim() === 'SPO Stockist Wise');
        if (target) target.click();
    }''')
    page.wait_for_timeout(3000)

    # Check if modal opened or direct report page
    print("Current URL:", page.url)

    # Check for date inputs or report grid
    info = page.evaluate('''() => {
        const inputs = Array.from(document.querySelectorAll('input')).map(i => ({
            id: i.id, name: i.name, val: i.value, ph: i.placeholder
        }));
        const trs = Array.from(document.querySelectorAll('tr'));
        const tablePreview = trs.slice(0, 10).map(tr => 
            Array.from(tr.querySelectorAll('td, th')).map(c => c.innerText.trim())
        ).filter(r => r.length > 2);
        return { inputs: inputs, tablesFound: trs.length, tableRows: tablePreview };
    }''')

    print("\nInputs found:", info['inputs'][:5])
    print(f"Total Table Rows found: {info['tablesFound']}")
    if info['tableRows']:
        print("\nTable Sample Rows:")
        for r in info['tableRows'][:6]:
            print("  •", r)

    # Save a clear JPEG screenshot
    page.screenshot(path='/workspaces/Dios/csv_output/spo_check.jpg', type='jpeg', quality=80)
    print("\n📸 Saved JPEG screenshot: csv_output/spo_check.jpg")

    browser.close()
