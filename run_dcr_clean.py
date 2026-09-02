from playwright.sync_api import sync_playwright
import time, os, calendar

MONTH_TARGET = "Aug-2026"
CBO_USER = "6958BANWARI"
CBO_PASS = "6958"
LOGIN_URL = "https://dios.myreporting.net/erp/login"
EXCEL_PATH = "/workspaces/Dios/csv_output/DCR_DateWise_Aug-2026.xls"

os.makedirs("/workspaces/Dios/csv_output", exist_ok=True)

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
    page.wait_for_timeout(3500)

    print("[2] Opening 'Date Wise Call Detail'...")
    page.locator("a:has-text('Reports'), span:has-text('Reports')").first.click()
    page.wait_for_timeout(800)

    page.evaluate('''() => {
        const elms = Array.from(document.querySelectorAll('a, span, li, td'));
        const dcr = elms.find(e => (e.innerText || '').trim() === 'DCR Reports');
        if (dcr) { dcr.dispatchEvent(new MouseEvent('mouseover', {bubbles: true})); dcr.click(); }
    }''')
    page.wait_for_timeout(800)

    page.evaluate('''() => {
        const elms = Array.from(document.querySelectorAll('a, span, li, td'));
        const item = elms.find(e => (e.innerText || '').trim() === 'Date Wise Call Detail');
        if (item) item.click();
    }''')
    page.wait_for_timeout(2500)

    print("[3] Setting BOTH Dates (From: 01/08/2026, To: 31/08/2026)...")
    res = page.evaluate('''() => {
        const wrappers = Array.from(document.querySelectorAll('.e-datepicker-wrapper, .e-date-wrapper'));
        let val1 = '', val2 = '';
        if (wrappers.length >= 2) {
            const inp1 = wrappers[0].querySelector('input');
            const inp2 = wrappers[1].querySelector('input');
            if (inp1) {
                inp1.value = '01/08/2026';
                inp1.dispatchEvent(new Event('input', {bubbles: true}));
                inp1.dispatchEvent(new Event('change', {bubbles: true}));
                val1 = inp1.value;
            }
            if (inp2) {
                inp2.value = '31/08/2026';
                inp2.dispatchEvent(new Event('input', {bubbles: true}));
                inp2.dispatchEvent(new Event('change', {bubbles: true}));
                val2 = inp2.value;
            }
        }
        return { wrappersCount: wrappers.length, from: val1, to: val2 };
    }''')
    print("Dates set result:", res)
    time.sleep(1)

    print("[4] Submitting (Clicking GO)...")
    page.evaluate('''() => {
        const btns = Array.from(document.querySelectorAll('button, input[type=button], input[type=submit]'));
        const go = btns.find(b => (b.innerText || b.value || '').trim().toUpperCase().includes('GO'));
        if (go) go.click();
    }''')

    time.sleep(6)

    print("[5] Downloading DCR Excel file from green toolbar icon...")
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
        print(f"🎉 EXCEL DOWNLOADED TO: {EXCEL_PATH}")
        downloaded = True
    except Exception as e:
        print("Excel download attempt error:", e)

    page.screenshot(path='/workspaces/Dios/csv_output/dcr_final_screen.png')
    browser.close()
