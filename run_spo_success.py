from playwright.sync_api import sync_playwright
import time, json, csv, os

CBO_USER = "6958BANWARI"
CBO_PASS = "6958"
LOGIN_URL = "https://dios.myreporting.net/erp/login"
OUT_CSV = "/workspaces/Dios/csv_output/3_SALES_PERFORMANCE_LIVE.csv"
OUT_XLS = "/workspaces/Dios/csv_output/SPO_StockistWise_Aug-2026.xls"

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

    print("[2] Opening Reports -> Sales & Targets...")
    page.locator("a:has-text('Reports'), span:has-text('Reports')").first.click()
    page.wait_for_timeout(600)

    # Dispatch mouseover on Sales & Targets
    page.evaluate('''() => {
        const elms = Array.from(document.querySelectorAll('a, span, li, td'));
        const st = elms.find(e => (e.innerText || '').trim() === 'Sales & Targets');
        if (st) {
            st.dispatchEvent(new MouseEvent('mouseover', {bubbles: true}));
            st.click();
        }
    }''')
    page.wait_for_timeout(800)

    print("[3] Clicking 'SPO Stockist Wise' via DOM...")
    clicked = page.evaluate('''() => {
        const elms = Array.from(document.querySelectorAll('a, span, li'));
        const target = elms.find(e => (e.innerText || '').trim() === 'SPO Stockist Wise');
        if (target) {
            target.click();
            return true;
        }
        return false;
    }''')
    print("Clicked SPO Stockist Wise:", clicked)
    time.sleep(5)

    # Check for datepicker modal and set August dates if modal exists
    print("[4] Checking for Date Filter Modal...")
    modal_set = page.evaluate('''() => {
        const pickers = Array.from(document.querySelectorAll('*')).filter(e => e.ej2_instances && e.ej2_instances.length > 0 && e.ej2_instances[0].getModuleName && e.ej2_instances[0].getModuleName() === 'datepicker');
        if (pickers.length >= 2) {
            pickers[0].ej2_instances[0].value = new Date(2026, 7, 1);
            if (pickers[0].ej2_instances[0].dataBind) pickers[0].ej2_instances[0].dataBind();
            pickers[1].ej2_instances[0].value = new Date(2026, 7, 31);
            if (pickers[1].ej2_instances[0].dataBind) pickers[1].ej2_instances[0].dataBind();

            const btns = Array.from(document.querySelectorAll('button, input[type=button], input[type=submit]'));
            const go = btns.find(b => (b.innerText || b.value || '').trim().toUpperCase().includes('GO'));
            if (go) go.click();
            return true;
        }
        return false;
    }''')
    if modal_set:
        print("Date Filter Modal was open, set August dates & clicked GO!")
        time.sleep(6)
    else:
        print("Report page directly active!")

    # Scrape Table
    print("\n[5] Extracting Table Data from Screen...")
    all_table_data = []
    for f in page.frames:
        rows = f.evaluate('''() => {
            const trs = Array.from(document.querySelectorAll('tr'));
            return trs.map(r => Array.from(r.querySelectorAll('td, th')).map(c => c.innerText.trim())).filter(r => r.length >= 2);
        }''')
        if len(rows) > 3:
            all_table_data = rows
            print(f"Found {len(rows)} rows in frame '{f.name}'!")
            break

    if all_table_data:
        print("\n================== SPO REPORT ROWS ==================")
        for idx, r in enumerate(all_table_data):
            print(f"[{idx+1}] {r}")

        with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(all_table_data)
        print(f"\n💾 Saved clean table CSV: {OUT_CSV}")

    # Try downloading Excel
    print("\n[6] Clicking Green Excel Icon...")
    try:
        with page.expect_download(timeout=10000) as dl_info:
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
        dl.save_as(OUT_XLS)
        print(f"🎉 EXCEL DOWNLOADED: {OUT_XLS}")
    except Exception as e:
        print("Excel download attempt note:", e)

    browser.close()
