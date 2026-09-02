import sys, time, os, csv
from playwright.sync_api import sync_playwright

MONTH_TARGET = sys.argv[1] if len(sys.argv) > 1 else "Aug-2026"
FY_TARGET = "2026-2027"
CBO_USER = os.getenv("CBO_USER", "6958BANWARI")
CBO_PASS = os.getenv("CBO_PASS", "6958")
LOGIN_URL = "https://dios.myreporting.net/erp/login"
DIRECT_REPORT_URL = f"https://dios.myreporting.net/RPT/PerformanceReview.aspx?format=Primary%20Sales&wise=P&DOC_TYPE=SS&RPT_HEADER=Monthly%20Sales-Summary&CBOYN=Y&FY_YEAR={FY_TARGET}&COMPANY_CODE=DIOS&PA_ID=6958&DESIG_ID=1&DESIG=BE&PA_NAME=BANWARI%20LAL%20MEENA&HEAD_QTR=UDAIPUR&DIVISION_NAME=DIOS%20GROUP&FMCGYN=N&MENU_STYLE=NONE&ACTION_FROM=ANDROID&LOGIN_PA_ID=6958&LOGIN_COMPANY_ID=1"

os.makedirs("/workspaces/Dios/csv_output", exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
    context = browser.new_context(viewport={'width': 1440, 'height': 900}, accept_downloads=True)
    page = context.new_page()
    page.on('dialog', lambda d: d.accept())

    print("[1] Logging into CBO...")
    page.goto(LOGIN_URL, timeout=60000, wait_until="domcontentloaded")
    page.wait_for_timeout(1500)
    page.fill("input[type='text']", CBO_USER)
    page.fill("input[type='password']", CBO_PASS)
    page.keyboard.press("Enter")
    page.wait_for_timeout(3500)

    print("[2] Opening Report...")
    page.goto(DIRECT_REPORT_URL, timeout=60000, wait_until="domcontentloaded")
    page.wait_for_timeout(4000)

    form_frame = page.main_frame
    for f in page.frames:
        if f.locator('select#MFDATE').count() > 0:
            form_frame = f
            break

    print(f"[3] Selecting Month [{MONTH_TARGET}] and Product Wise...")
    form_frame.evaluate('''(target) => {
        const selectByText = (sel, textMatch) => {
            if (!sel) return;
            for (let o of sel.options) {
                if (o.text.toLowerCase().includes(textMatch.toLowerCase()) || o.text.toLowerCase().includes(target.substring(0,3).toLowerCase())) {
                    sel.value = o.value;
                    sel.dispatchEvent(new Event('change', {bubbles: true}));
                    break;
                }
            }
        };

        const selects = Array.from(document.querySelectorAll('select'));
        selects.forEach(s => {
            const id = (s.id || s.name || '').toUpperCase();
            if (id.includes('FDATE')) selectByText(s, target);
            if (id.includes('TDATE')) selectByText(s, target);
            if (id.includes('GROUPING') || id.includes('WISE')) selectByText(s, 'Product');
            if (id.includes('FORMAT')) selectByText(s, 'Primary');
        });
    }''', MONTH_TARGET)

    time.sleep(1)

    print("[4] Submitting Form...")
    active_page = page
    try:
        with context.expect_page(timeout=5000) as popup_info:
            form_frame.evaluate('''() => {
                const btn = document.getElementById('btnGo1') || document.getElementById('btnGo') || document.querySelector("button:has-text('Go'), input[value*='Go']");
                if (btn) btn.click();
            }''')
        active_page = popup_info.value
    except Exception:
        form_frame.evaluate('''() => {
            const btn = document.getElementById('btnGo1') || document.getElementById('btnGo') || document.querySelector("button:has-text('Go'), input[value*='Go']");
            if (btn) btn.click();
        }''')

    active_page.wait_for_load_state("domcontentloaded")
    time.sleep(6)

    # Click UDAIPUR link using JS evaluation (bypasses any modal/backdrop blocker)
    print("[5] Expanding UDAIPUR to view Products...")
    clicked_drilldown = False
    for f in active_page.frames:
        clicked_drilldown = f.evaluate('''() => {
            const links = Array.from(document.querySelectorAll('a, span, td'));
            const uLink = links.find(el => el.innerText && el.innerText.trim().toUpperCase() === 'UDAIPUR');
            if (uLink) {
                uLink.click();
                return true;
            }
            return false;
        }''')
        if clicked_drilldown:
            print("👉 Clicked UDAIPUR link successfully!")
            time.sleep(5)
            break

    # Download Excel from top right button
    print("[6] Downloading Excel...")
    excel_path = f"/workspaces/Dios/csv_output/Primary_{MONTH_TARGET}.xls"
    for f in active_page.frames:
        try:
            excel_btn = f.locator("a:has-text('Excel'), button:has-text('Excel'), [id*='Excel'], [id*='excel'], img[title*='Excel']").first
            if excel_btn.count() > 0:
                with active_page.expect_download(timeout=15000) as dl_info:
                    f.evaluate('''() => {
                        const btn = Array.from(document.querySelectorAll('a, button, input, img')).find(e => 
                            (e.innerText || e.value || e.title || e.id || '').toLowerCase().includes('excel')
                        );
                        if (btn) btn.click();
                    }''')
                dl = dl_info.value
                dl.save_as(excel_path)
                print(f"🎉 EXCEL DOWNLOADED TO: {excel_path}")
                break
        except Exception as e:
            print("Excel click info:", e)

    # Scrape Table accurately
    print("[7] Extracting Clean Product Data...")
    extracted_items = []
    for f in active_page.frames:
        table_data = f.evaluate('''() => {
            const result = [];
            const trs = Array.from(document.querySelectorAll('tr'));
            for (let tr of trs) {
                const cells = Array.from(tr.querySelectorAll('td, th')).map(c => c.innerText.trim());
                if (cells.length >= 2) {
                    result.push(cells);
                }
            }
            return result;
        }''')

        for r in table_data:
            # Check for standard product row [Product Name, Qty, Value]
            first_cell = r[0]
            if not first_cell:
                continue
            if any(k in first_cell.upper() for k in ['PRODUCT', 'COUNT', 'PRIMARY SALES', 'TOTAL', 'MONTHLY SALES', 'HEAD QTR', 'OPTIONS', 'COLUMNS', 'EXCEL', 'PDF', 'S.N']):
                continue
            
            # Find the numeric cells
            nums = []
            for c in r[1:]:
                clean_c = c.replace(',', '').replace('₹', '').strip()
                try:
                    nums.append(float(clean_c))
                except ValueError:
                    pass

            if len(nums) >= 2:
                qty = nums[0]
                val = nums[1]
                extracted_items.append({'name': first_cell, 'qty': qty, 'value': val})
            elif len(nums) == 1:
                extracted_items.append({'name': first_cell, 'qty': nums[0], 'value': 0})

    if len(extracted_items) > 0:
        csv_path = f"/workspaces/Dios/csv_output/Primary_Live_{MONTH_TARGET}.csv"
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["PRODUCT NAME", "PRIMARY QTY", "PRIMARY VALUE"])
            for it in extracted_items:
                writer.writerow([it["name"], it["qty"], it["value"]])
        print(f"✅ Extracted {len(extracted_items)} Products into: {csv_path}")
        print("\n--- First 5 Products Preview ---")
        for it in extracted_items[:5]:
            print(f"  • {it['name']} | Qty: {it['qty']} | Value: ₹{it['value']}")
    else:
        print("⚠️ No products extracted. Capturing screen...")
        active_page.screenshot(path="/workspaces/Dios/csv_output/cbo_after_drilldown.png")

    browser.close()
    print("\n🏁 Done!")
