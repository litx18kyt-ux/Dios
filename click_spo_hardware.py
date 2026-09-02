from playwright.sync_api import sync_playwright
import time, json

CBO_USER = "6958BANWARI"
CBO_PASS = "6958"
LOGIN_URL = "https://dios.myreporting.net/erp/login"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
    context = browser.new_context(viewport={'width': 1440, 'height': 900})
    page = context.new_page()

    # Track all requests after click
    page.on("request", lambda r: print(f"📡 REQUEST: {r.method} -> {r.url}"))
    page.on("response", lambda r: print(f"📦 RESPONSE: {r.status} -> {r.url[:80]}"))

    print("[1] Logging into CBO...")
    page.goto(LOGIN_URL, timeout=60000, wait_until="domcontentloaded")
    page.wait_for_timeout(1500)
    page.fill("input[type='text']:visible", CBO_USER)
    page.fill("input[type='password']:visible", CBO_PASS)
    page.locator("button:visible:has-text('Login'), input[type='submit']:visible, .btn-success:visible").first.click()
    page.wait_for_timeout(3500)

    print("[2] Opening Reports -> Sales & Targets...")
    page.locator("a:has-text('Reports'), span:has-text('Reports')").first.click()
    page.wait_for_timeout(800)

    # Hover Sales & Targets
    page.evaluate('''() => {
        const elms = Array.from(document.querySelectorAll('a, span, li, td'));
        const st = elms.find(e => (e.innerText || '').trim() === 'Sales & Targets');
        if (st) {
            st.dispatchEvent(new MouseEvent('mouseover', {bubbles: true}));
            st.dispatchEvent(new MouseEvent('mouseenter', {bubbles: true}));
            st.click();
        }
    }''')
    page.wait_for_timeout(1000)

    print("[3] Getting Pixel Coordinates of 'SPO Stockist Wise'...")
    target_locator = page.locator("#\\$Reports\\/CnfSpoStk_Report, li:has-text('SPO Stockist Wise')").first
    box = target_locator.bounding_box()
    print("Coordinates Box:", box)

    if box:
        print(f"👉 Hardware Mouse Clicking at ({box['x'] + box['width']/2}, {box['y'] + box['height']/2})...")
        page.mouse.click(box['x'] + box['width']/2, box['y'] + box['height']/2)
    else:
        print("Bounding box not visible, dispatching pointer events directly...")
        page.evaluate('''() => {
            const item = document.getElementById('$Reports/CnfSpoStk_Report');
            if (item) {
                item.dispatchEvent(new PointerEvent('pointerdown', {bubbles: true}));
                item.dispatchEvent(new MouseEvent('mousedown', {bubbles: true}));
                item.dispatchEvent(new PointerEvent('pointerup', {bubbles: true}));
                item.dispatchEvent(new MouseEvent('mouseup', {bubbles: true}));
                item.dispatchEvent(new MouseEvent('click', {bubbles: true}));
            }
        }''')

    time.sleep(6)

    print(f"\n[4] State after click:")
    print("Current URL:", page.url)

    # Check for modals or tables
    tables = page.evaluate('''() => {
        const trs = Array.from(document.querySelectorAll('tr'));
        return trs.map(r => Array.from(r.querySelectorAll('td, th')).map(c => c.innerText.trim())).filter(r => r.length >= 3);
    }''')
    print(f"Total Table Rows found: {len(tables)}")
    for r in tables[:8]:
        print("  •", r)

    page.screenshot(path='/workspaces/Dios/csv_output/spo_after_hardware_click.png')
    print("\n📸 Saved Screenshot: csv_output/spo_after_hardware_click.png")

    browser.close()
