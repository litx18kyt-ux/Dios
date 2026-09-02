from playwright.sync_api import sync_playwright
import time, json, os, csv

CBO_USER = "6958BANWARI"
CBO_PASS = "6958"
LOGIN_URL = "https://dios.myreporting.net/erp/login"
OUT_TXT = "/workspaces/Dios/spo_live_result.txt"
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

    print("[3] Clicking 'SPO Stockist Wise'...")
    target_locator = page.locator("#\\$Reports\\/CnfSpoStk_Report, li:has-text('SPO Stockist Wise')").first
    box = target_locator.bounding_box()
    if box:
        print(f"👉 Clicking at ({box['x'] + box['width']/2}, {box['y'] + box['height']/2})...")
        page.mouse.click(box['x'] + box['width']/2, box['y'] + box['height']/2)
    else:
        page.locator("text='SPO Stockist Wise'").first.click()

    # SMART WAIT: Wait for the CBO Spinner to completely finish loading!
    print("\n[4] Waiting for CBO Loading Spinner to finish (Giving 12-15 seconds)...")
    for sec in range(15):
        time.sleep(1)
        spinner_count = page.evaluate('''() => {
            return document.querySelectorAll('.spinner, .loading, .e-spinner-pane, [class*=\"spinner\"]').length;
        }''')
        if sec > 6 and spinner_count == 0:
            print(f"✅ Spinner finished at {sec} seconds!")
            break

    time.sleep(3)

    # Scrape Table Rows across all frames
    print("\n[5] Extracting SPO Report Table Data...")
    report_rows = []
    for f in page.frames:
        rows = f.evaluate('''() => {
            const trs = Array.from(document.querySelectorAll('tr'));
            return trs.map(r => Array.from(r.querySelectorAll('td, th')).map(c => c.innerText.trim())).filter(r => r.length >= 3);
        }''')
        # Check if table has distributor names
        for r in rows:
            r_str = " ".join(r).upper()
            if any(dist in r_str for dist in ['VARDHMAN', 'MODI', 'DWARIKA', 'R.P', 'SUN', 'TOTAL']):
                report_rows.append(r)

    # Click Green Excel icon to download file
    print("\n[6] Downloading Green Excel file...")
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
        dl.save_as(OUT_XLS)
        print(f"🎉 EXCEL DOWNLOADED TO: {OUT_XLS}")
        downloaded = True
    except Exception as e:
        print("Excel download note:", e)

    # Write full result to txt file
    with open(OUT_TXT, "w", encoding="utf-8") as f:
        f.write(f"EXCEL_DOWNLOADED: {downloaded}\n")
        f.write(f"TOTAL_ROWS_FOUND: {len(report_rows)}\n\n")
        f.write("=== SCRAPED ROWS ===\n")
        for r in report_rows:
            f.write(" | ".join(r) + "\n")

    print(f"\n📁 Results successfully written to: {OUT_TXT}")
    browser.close()
