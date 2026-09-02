from playwright.sync_api import sync_playwright
import time, json

CBO_USER = "6958BANWARI"
CBO_PASS = "6958"
LOGIN_URL = "https://dios.myreporting.net/erp/login"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
    context = browser.new_context(viewport={'width': 1440, 'height': 900}, accept_downloads=True)
    page = context.new_page()

    requests_log = []
    page.on("request", lambda r: requests_log.append({'method': r.method, 'url': r.url}))

    print("[1] Logging in to CBO...")
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
            st.click();
        }
    }''')
    page.wait_for_timeout(1000)

    print("[3] Clicking 'SPO Stockist Wise'...")
    # Click the exact menu item
    clicked = page.evaluate('''() => {
        const item = document.getElementById('$Reports/CnfSpoStk_Report') || 
                     Array.from(document.querySelectorAll('li, a, span')).find(e => (e.innerText || '').trim() === 'SPO Stockist Wise');
        if (item) {
            item.click();
            return { clicked: true, text: item.innerText, id: item.id };
        }
        return { clicked: false };
    }''')
    print("Click Result:", clicked)
    time.sleep(5)

    print(f"\n[4] Page URL: {page.url}")
    print(f"Total Frames: {len(page.frames)}")
    for idx, f in enumerate(page.frames):
        print(f"  Frame {idx}: '{f.name}' | URL: {f.url}")

    # Check for tables across all frames
    print("\n[5] Checking Table Rows in all frames...")
    found_any_table = False
    for f in page.frames:
        rows = f.evaluate('''() => {
            const trs = Array.from(document.querySelectorAll('tr'));
            return trs.map(r => Array.from(r.querySelectorAll('td, th')).map(c => c.innerText.trim())).filter(r => r.length > 2);
        }''')
        if len(rows) > 0:
            print(f"🎯 Frame '{f.name}' has {len(rows)} rows!")
            found_any_table = True
            for r in rows[:10]:
                print("  •", r)

    # Network requests triggered
    print("\n[6] Network requests after click:")
    for req in requests_log[-12:]:
        print(f"  {req['method']} -> {req['url']}")

    browser.close()
