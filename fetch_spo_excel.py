from playwright.sync_api import sync_playwright
import time, json, os

CBO_USER = "6958BANWARI"
CBO_PASS = "6958"
LOGIN_URL = "https://dios.myreporting.net/erp/login"
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

    print("[2] Clicking exact menu: $Reports/CnfSpoStk_Report...")
    clicked = page.evaluate('''() => {
        const item = document.getElementById('$Reports/CnfSpoStk_Report');
        if (item) {
            item.click();
            return true;
        }
        return false;
    }''')
    print("Menu Clicked:", clicked)
    page.wait_for_timeout(3000)

    # If there is a date modal, fill dates and click GO
    print("[3] Checking and setting Dates if modal present...")
    page.evaluate('''() => {
        const allElements = Array.from(document.querySelectorAll('*')).filter(e => e.ej2_instances && e.ej2_instances.length > 0);
        const pickers = allElements.filter(e => e.ej2_instances[0].getModuleName && e.ej2_instances[0].getModuleName() === 'datepicker');
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

    # Print Table Rows
    print("\n[4] Scraping Report Table...")
    for f in page.frames:
        rows = f.evaluate('''() => {
            const trs = Array.from(document.querySelectorAll('tr'));
            return trs.map(r => Array.from(r.querySelectorAll('td, th')).map(c => c.innerText.trim())).filter(r => r.length > 2);
        }''')
        if len(rows) > 0:
            print(f"Frame '{f.name}': Found {len(rows)} rows!")
            for r in rows:
                print("  •", r)

    # Click Green Excel Download Icon
    print("\n[5] Clicking Green Excel Export Icon...")
    downloaded = False
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
        downloaded = True
    except Exception as e:
        print("Excel Download note:", e)

    browser.close()
