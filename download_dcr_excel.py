from playwright.sync_api import sync_playwright
import time, os, calendar

MONTH_TARGET = "Aug-2026"
month_map = {"JAN":1,"FEB":2,"MAR":3,"APR":4,"MAY":5,"JUN":6,"JUL":7,"AUG":8,"SEP":9,"OCT":10,"NOV":11,"DEC":12}
parts = MONTH_TARGET.split('-')
m_num = month_map.get(parts[0].upper()[:3], 8)
year = int(parts[1]) if len(parts) > 1 else 2026
num_days = calendar.monthrange(year, m_num)[1]

from_date_str = f"01/{m_num:02d}/{year}"
to_date_str = f"{num_days:02d}/{m_num:02d}/{year}"

CBO_USER = "6958BANWARI"
CBO_PASS = "6958"
LOGIN_URL = "https://dios.myreporting.net/erp/login"

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
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)

    print("[2] Opening 'Date Wise Call Detail'...")
    page.locator("a:has-text('Reports'), span:has-text('Reports')").first.click()
    page.wait_for_timeout(800)

    page.evaluate('''() => {
        const elms = Array.from(document.querySelectorAll('a, span, li, td'));
        const dcr = elms.find(e => (e.innerText || '').trim() === 'DCR Reports');
        if (dcr) {
            dcr.dispatchEvent(new MouseEvent('mouseover', {bubbles: true}));
            dcr.click();
        }
    }''')
    page.wait_for_timeout(800)

    page.evaluate('''() => {
        const elms = Array.from(document.querySelectorAll('a, span, li, td'));
        const item = elms.find(e => (e.innerText || '').trim() === 'Date Wise Call Detail');
        if (item) item.click();
    }''')
    page.wait_for_timeout(2500)

    print(f"[3] Setting Both Datepicker Widgets: [{from_date_str}] to [{to_date_str}]...")
    date_result = page.evaluate('''(dates) => {
        // Find distinct datepicker containers
        const wrappers = Array.from(document.querySelectorAll('.e-datepicker-wrapper, .e-date-wrapper'));
        if (wrappers.length >= 2) {
            const inp1 = wrappers[0].querySelector('input');
            const inp2 = wrappers[1].querySelector('input');

            if (inp1) {
                inp1.focus();
                inp1.value = dates[0];
                inp1.dispatchEvent(new Event('input', {bubbles: true}));
                inp1.dispatchEvent(new Event('change', {bubbles: true}));
                inp1.blur();
            }
            if (inp2) {
                inp2.focus();
                inp2.value = dates[1];
                inp2.dispatchEvent(new Event('input', {bubbles: true}));
                inp2.dispatchEvent(new Event('change', {bubbles: true}));
                inp2.blur();
            }

            // Syncfusion native instances update
            const pickers = Array.from(document.querySelectorAll('input')).filter(el => el.ej2_instances && el.ej2_instances.length > 0);
            if (pickers.length >= 2) {
                const p1 = dates[0].split('/');
                const p2 = dates[1].split('/');
                pickers[0].ej2_instances[0].value = new Date(p1[2], parseInt(p1[1])-1, p1[0]);
                pickers[1].ej2_instances[0].value = new Date(p2[2], parseInt(p2[1])-1, p2[0]);
            }
            return { success: true, count: wrappers.length, val1: inp1 ? inp1.value : '', val2: inp2 ? inp2.value : '' };
        }
        return { success: false, count: wrappers.length };
    }''', [from_date_str, to_date_str])

    print("Datepicker Set Output:", date_result)
    time.sleep(1)

    print("[4] Submitting (Clicking GO)...")
    page.evaluate('''() => {
        const btns = Array.from(document.querySelectorAll('button, input[type=button], input[type=submit]'));
        const go = btns.find(b => (b.innerText || b.value || '').trim().toUpperCase().includes('GO'));
        if (go) go.click();
    }''')

    time.sleep(6)

    # Click the Green Excel Icon on top-right toolbar
    print("[5] Downloading DCR Excel file from top-right toolbar...")
    excel_path = f"/workspaces/Dios/csv_output/DCR_DateWise_{MONTH_TARGET}.xls"
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
        dl.save_as(excel_path)
        print(f"🎉 EXCEL FILE DOWNLOADED: {excel_path}")
        downloaded = True
    except Exception as e:
        print("Excel download attempt info:", e)

    page.screenshot(path='/workspaces/Dios/csv_output/dcr_final_screen.png')
    print("📸 Screenshot saved to: csv_output/dcr_final_screen.png")

    browser.close()

    # Step 6: Inspect Excel File format
    if downloaded and os.path.exists(excel_path):
        size = os.path.getsize(excel_path)
        print(f"\n[6] Downloaded Excel Size: {size} bytes")
        with open(excel_path, 'rb') as f:
            header_bytes = f.read(16)
        print("File Signature Bytes:", header_bytes)
