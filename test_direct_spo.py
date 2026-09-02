from playwright.sync_api import sync_playwright
import time, json, os

CBO_USER = "6958BANWARI"
CBO_PASS = "6958"
LOGIN_URL = "https://dios.myreporting.net/erp/login"
DIRECT_SPO_URL = "https://dios.myreporting.net/erp/reports/CnfSpoStk_Report"
MONTH_TARGET = "Aug-2026"
EXCEL_PATH = f"/workspaces/Dios/csv_output/SPO_StockistWise_{MONTH_TARGET}.xls"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
    context = browser.new_context(viewport={'width': 1440, 'height': 900}, accept_downloads=True)
    page = context.new_page()
    page.on('dialog', lambda d: d.accept())

    print("[1] Logging into CBO...")
    page.goto(LOGIN_URL, timeout=60000, wait_until="domcontentloaded")
    page.wait_for_timeout(1500)
    page.fill("input[type='text']:visible", CBO_USER)
    page.fill("input[type='password']:visible", CBO_PASS)
    page.locator("button:visible:has-text('Login'), input[type='submit']:visible, .btn-success:visible").first.click()
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)

    print(f"[2] Navigating directly to: {DIRECT_SPO_URL}...")
    page.goto(DIRECT_SPO_URL, timeout=60000, wait_until="domcontentloaded")
    page.wait_for_timeout(4000)

    print("Current URL:", page.url)

    # Check if a datepicker modal or filter is present
    page.evaluate('''() => {
        const pickers = Array.from(document.querySelectorAll('*')).filter(e => e.ej2_instances && e.ej2_instances.length > 0 && e.ej2_instances[0].getModuleName && e.ej2_instances[0].getModuleName() === 'datepicker');
        if (pickers.length >= 2) {
            pickers[0].ej2_instances[0].value = new Date(2026, 7, 1);
            if (pickers[0].ej2_instances[0].dataBind) pickers[0].ej2_instances[0].dataBind();
            pickers[1].ej2_instances[0].value = new Date(2026, 7, 31);
            if (pickers[1].ej2_instances[0].dataBind) pickers[1].ej2_instances[0].dataBind();

            const btns = Array.from(document.querySelectorAll('button, input[type=button], input[type=submit]'));
            const go = btns.find(b => (b.innerText || b.value || '').trim().toUpperCase().includes('GO'));
            if (go) go.click();
        }
    }''')
    time.sleep(5)

    # Scrape Table Rows
    print("\n[3] Reading SPO Table Rows...")
    table_rows = []
    for f in page.frames:
        rows = f.evaluate('''() => {
            const trs = Array.from(document.querySelectorAll('tr'));
            return trs.map(r => Array.from(r.querySelectorAll('td, th')).map(c => c.innerText.trim())).filter(r => r.length >= 4);
        }''')
        if len(rows) > 3:
            table_rows = rows
            print(f"🎯 Found {len(rows)} rows in frame '{f.name}'!")
            break

    for idx, r in enumerate(table_rows):
        print(f"[{idx+1}] {r}")

    # Click Green Excel icon
    print("\n[4] Downloading SPO Excel File...")
    try:
        with page.expect_download(timeout=15000) as dl_info:
            page.evaluate('''() => {
                const elms = Array.from(document.querySelectorAll('a, button, i, span, img'));
                const btn = elms.find(e => {
                    const cls = (e.className || '').toLowerCase();
                    const title = (e.getAttribute('title') || '').toLowerCase();
                    return cls.includes('excel') || title.includes('excel') || cls.includes('fa-file-excel');
                });
                if (btn) btn.click();
            }''')
        dl = dl_info.value
        dl.save_as(EXCEL_PATH)
        print(f"🎉 EXCEL DOWNLOADED: {EXCEL_PATH}")
    except Exception as e:
        print("Excel download note:", e)

    browser.close()
