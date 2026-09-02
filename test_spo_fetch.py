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
    page.wait_for_timeout(3500)

    print("[2] Opening Reports -> Sales & Targets -> SPO Stockist Wise...")
    page.locator("a:has-text('Reports'), span:has-text('Reports')").first.click()
    page.wait_for_timeout(800)

    page.evaluate('''() => {
        const elms = Array.from(document.querySelectorAll('a, span, li, td'));
        const st = elms.find(e => (e.innerText || '').trim() === 'Sales & Targets');
        if (st) {
            st.dispatchEvent(new MouseEvent('mouseover', {bubbles: true}));
            st.click();
        }
    }''')
    page.wait_for_timeout(800)

    page.evaluate('''() => {
        const elms = Array.from(document.querySelectorAll('a, span, li, td'));
        const item = elms.find(e => (e.innerText || '').trim().includes('SPO Stockist Wise'));
        if (item) item.click();
    }''')
    page.wait_for_timeout(2500)

    print(f"[3] Setting Syncfusion Dates: {from_date_str} to {to_date_str}...")
    page.evaluate('''(info) => {
        const allElements = Array.from(document.querySelectorAll('*')).filter(e => e.ej2_instances && e.ej2_instances.length > 0);
        const pickers = allElements.filter(e => e.ej2_instances[0].getModuleName && e.ej2_instances[0].getModuleName() === 'datepicker');
        if (pickers.length >= 2) {
            const dFrom = new Date(info.year, info.m_idx, 1);
            const dTo = new Date(info.year, info.m_idx, info.last_day);

            pickers[0].ej2_instances[0].value = dFrom;
            if (pickers[0].ej2_instances[0].dataBind) pickers[0].ej2_instances[0].dataBind();

            pickers[1].ej2_instances[0].value = dTo;
            if (pickers[1].ej2_instances[0].dataBind) pickers[1].ej2_instances[0].dataBind();
        }
    }''', {'year': year, 'm_idx': m_num - 1, 'last_day': num_days})

    time.sleep(1)

    print("[4] Clicking GO...")
    page.evaluate('''() => {
        const btns = Array.from(document.querySelectorAll('button, input[type=button], input[type=submit]'));
        const go = btns.find(b => (b.innerText || b.value || '').trim().toUpperCase().includes('GO'));
        if (go) go.click();
    }''')

    time.sleep(6)

    print("[5] Downloading SPO Stockist Wise Excel file...")
    excel_path = f"/workspaces/Dios/csv_output/SPO_StockistWise_{MONTH_TARGET}.xls"
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
        print(f"🎉 EXCEL DOWNLOADED TO: {excel_path}")
        downloaded = True
    except Exception as e:
        print("Excel download attempt error:", e)

    page.screenshot(path='/workspaces/Dios/csv_output/spo_final_screen.png')
    browser.close()
