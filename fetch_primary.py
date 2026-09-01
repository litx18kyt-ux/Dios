import os, sys, time, csv
from playwright.sync_api import sync_playwright

MONTH_TARGET = sys.argv[1] if len(sys.argv) > 1 else "Aug-2026"
FY_TARGET = "2026-2027"

CBO_USER = os.getenv("CBO_USER", "6958BANWARI")
CBO_PASS = os.getenv("CBO_PASS", "6958")

SESSION_FILE = "cbo_session.json"
LOGIN_URL = "https://dios.myreporting.net/erp/login"
DIRECT_REPORT_URL = f"https://dios.myreporting.net/RPT/PerformanceReview.aspx?format=Primary%20Sales&wise=P&DOC_TYPE=SS&RPT_HEADER=Monthly%20Sales-Summary&CBOYN=Y&FY_YEAR={FY_TARGET}&COMPANY_CODE=DIOS&PA_ID=6958&DESIG_ID=1&DESIG=BE&PA_NAME=BANWARI%20LAL%20MEENA&HEAD_QTR=UDAIPUR&DIVISION_NAME=DIOS%20GROUP&FMCGYN=N&MENU_STYLE=NONE&ACTION_FROM=ANDROID&LOGIN_PA_ID=6958&LOGIN_COMPANY_ID=1"

os.makedirs("csv_output", exist_ok=True)

print("="*65)
print(f"🤖 DIOS CBO ERP BOT: Exporting Primary Data [{MONTH_TARGET}]")
print("="*65)

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--disable-popup-blocking", "--no-sandbox", "--disable-web-security"]
    )
    
    storage = SESSION_FILE if os.path.exists(SESSION_FILE) else None
    if storage:
        print("🔑 Using saved session...")
        context = browser.new_context(storage_state=storage, viewport={"width": 1440, "height": 900}, accept_downloads=True)
    else:
        print("⚡ Clean Session initialized...")
        context = browser.new_context(viewport={"width": 1440, "height": 900}, accept_downloads=True)

    page = context.new_page()
    page.on("dialog", lambda dialog: dialog.accept())

    try:
        # STEP 1: Check Login
        print("\n[1/5] Checking Login Status...")
        page.goto(LOGIN_URL, timeout=60000, wait_until="networkidle")
        page.wait_for_timeout(1000)

        if "login" in page.url.lower() or page.locator("input[type='password']").count() > 0:
            print("🔑 Performing Login...")
            page.fill("input[type='text']:visible", CBO_USER)
            page.fill("input[type='password']:visible", CBO_PASS)
            
            login_btn = page.locator("button:visible:has-text('Login'), input[type='submit']:visible, .btn-success:visible").first
            if login_btn.count() > 0:
                login_btn.click()
            else:
                page.keyboard.press("Enter")

            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(3000)
            context.storage_state(path=SESSION_FILE)
            print("💾 Session Saved!")

        # STEP 2: Open Report Form
        print("\n[2/5] Opening Monthly Sales Report Modal...")
        page.goto(DIRECT_REPORT_URL, timeout=60000, wait_until="domcontentloaded")
        page.wait_for_timeout(3500)

        # STEP 3: Find Frame & Set Month Dropdowns
        print(f"\n[3/5] Selecting Month [{MONTH_TARGET}]...")
        target_frame = None
        for f in page.frames:
            try:
                has_selects = f.evaluate("""(target) => {
                    const selects = Array.from(document.querySelectorAll('select'));
                    const mSelects = selects.filter(s => Array.from(s.options).some(o => o.text.includes('202') || o.text.includes('Aug') || o.text.includes('Apr')));
                    if (mSelects.length >= 2) {
                        for (let opt of mSelects[0].options) {
                            if (opt.text.toLowerCase().includes(target.toLowerCase()) || opt.text.toLowerCase().includes(target.substring(0,3).toLowerCase())) {
                                mSelects[0].value = opt.value;
                                mSelects[0].dispatchEvent(new Event('change', { bubbles: true }));
                                break;
                            }
                        }
                        for (let opt of mSelects[1].options) {
                            if (opt.text.toLowerCase().includes(target.toLowerCase()) || opt.text.toLowerCase().includes(target.substring(0,3).toLowerCase())) {
                                mSelects[1].value = opt.value;
                                mSelects[1].dispatchEvent(new Event('change', { bubbles: true }));
                                break;
                            }
                        }
                        return true;
                    }
                    return false;
                }""", MONTH_TARGET)
                if has_selects:
                    target_frame = f
                    print(f"🎯 Month set in frame: '{f.name or 'main'}'")
                    break
            except Exception:
                pass

        if not target_frame:
            target_frame = page.main_frame

        # STEP 4: Click [Go] Button
        print("\n[4/5] Clicking [Go] Button...")
        out_excel = f"csv_output/Primary_{MONTH_TARGET}.xlsx"
        out_csv = f"csv_output/Primary_{MONTH_TARGET}.csv"

        active_page = page
        try:
            with context.expect_page(timeout=5000) as popup_info:
                target_frame.evaluate("""() => {
                    const btns = Array.from(document.querySelectorAll('button, input, a'));
                    const go = btns.find(b => (b.innerText || b.value || '').trim().toLowerCase() === 'go' || b.id.toLowerCase().includes('btngo'));
                    if (go) go.click();
                }""")
            active_page = popup_info.value
            print("🪟 Switched to Report Window!")
        except Exception:
            target_frame.evaluate("""() => {
                const btns = Array.from(document.querySelectorAll('button, input, a'));
                const go = btns.find(b => (b.innerText || b.value || '').trim().toLowerCase() === 'go' || b.id.toLowerCase().includes('btngo'));
                if (go) go.click();
            }""")

        # Wait for Report Table
        print("⏳ Waiting for Report Table to Load...")
        active_page.wait_for_load_state("domcontentloaded")
        active_page.wait_for_timeout(6000)
        active_page.screenshot(path="csv_output/report_screen.png")

        # STEP 5: Download Official Excel & Scrape Table
        print("\n[5/5] Downloading Excel & Exporting CSV...")

        # 5a. Direct Excel Button Click
        excel_downloaded = False
        for f in active_page.frames:
            try:
                excel_btn = f.locator("button:has-text('Excel'), a:has-text('Excel'), :text('Excel')").first
                if excel_btn.count() > 0 and excel_btn.is_visible():
                    print("📥 Clicking the blue [Excel] button...")
                    with active_page.expect_download(timeout=15000) as dl_info:
                        excel_btn.click(force=True)
                    dl = dl_info.value
                    dl.save_as(out_excel)
                    print(f"🎉 EXCEL DOWNLOADED SUCCESSFULLY: {out_excel}")
                    excel_downloaded = True
                    break
            except Exception as e:
                print(f"   (Excel download trigger note: {e})")

        # 5b. Extract the Table directly from the screen
        print("📊 Extracting all rows from the Primary Sales table...")
        scraped_products = []

        for f in active_page.frames:
            rows = f.evaluate("""() => {
                const result = [];
                const allRows = Array.from(document.querySelectorAll('tr'));
                for (let r of allRows) {
                    const cells = Array.from(r.querySelectorAll('td, th')).map(c => c.innerText.trim());
                    if (cells.length >= 2) {
                        result.push(cells);
                    }
                }
                return result;
            }""")

            for r in rows:
                if len(r) >= 2:
                    p_name = r[0]
                    # Filter only actual products (skip title/headers/counts)
                    if p_name and not p_name.upper().startswith("PRODUCT") and not p_name.upper().startswith("COUNT") and not p_name.upper().startswith("PRIMARY"):
                        scraped_products.append(r)

        if len(scraped_products) > 0:
            with open(out_csv, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["PRODUCT NAME", "PRIMARY QTY", "PRIMARY VALUE"])
                for sp in scraped_products:
                    writer.writerow([sp[0], sp[1] if len(sp) > 1 else "0", sp[2] if len(sp) > 2 else "0"])
            print(f"🎉 CSV FILE CREATED: {out_csv} ({len(scraped_products)} Products extracted!)")
            print("\n📋 Top 10 Products Preview:")
            for p in scraped_products[:10]:
                print(f"   • {p[0]:<30} | Qty: {p[1]:<6} | Value: ₹{p[2] if len(p) > 2 else '0'}")
        else:
            print("⚠️ Table not found. Please check 'csv_output/report_screen.png'")

    except Exception as err:
        print(f"\n❌ Error: {err}")
    finally:
        browser.close()
        print("\n" + "="*65)
        print("🏁 Bot Finished Execution.")
        print("="*65)
