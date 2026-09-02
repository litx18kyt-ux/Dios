import sys, time, os, csv
from bs4 import BeautifulSoup
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

    print("[1] Logging in to CBO...")
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
        if f.locator('select#MFDATE').count() > 0 or f.locator('select[name*="FDATE"]').count() > 0:
            form_frame = f
            break

    print(f"[3] Selecting Month [{MONTH_TARGET}]...")
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

    # Click UDAIPUR to drill down to product view
    print("[5] Expanding UDAIPUR for Product details...")
    for f in active_page.frames:
        clicked = f.evaluate('''() => {
            const links = Array.from(document.querySelectorAll('a, span, td'));
            const uLink = links.find(el => el.innerText && el.innerText.trim().toUpperCase() === 'UDAIPUR');
            if (uLink) {
                uLink.click();
                return true;
            }
            return false;
        }''')
        if clicked:
            time.sleep(5)
            break

    # Click Excel button to download the file
    print("[6] Clicking Excel Export Button...")
    excel_path = f"/workspaces/Dios/csv_output/Primary_Excel_{MONTH_TARGET}.xls"
    downloaded = False

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
                print(f"🎉 EXCEL FILE DOWNLOADED: {excel_path}")
                downloaded = True
                break
        except Exception as e:
            print("Excel click attempt error:", e)

    browser.close()

    # Step 7: Parse the Downloaded Excel File
    if downloaded and os.path.exists(excel_path):
        print("\n[7] Parsing Downloaded Excel File...")
        with open(excel_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        soup = BeautifulSoup(content, 'html.parser')
        rows = soup.find_all('tr')
        excel_items = []
        for r in rows:
            cells = [c.get_text(strip=True) for c in r.find_all(['td', 'th'])]
            if len(cells) >= 2:
                p_name = cells[0]
                if p_name and not any(k in p_name.upper() for k in ['PRODUCT', 'COUNT', 'PRIMARY', 'TOTAL', 'MONTHLY SALES', 'CLOSE', 'ADVANCE', 'WISE', 'S.N', 'HEAD QTR', 'UDAIPUR']):
                    try:
                        qty = float(cells[1].replace(',', ''))
                        val = float(cells[2].replace(',', '')) if len(cells) > 2 else 0
                        if len(p_name) > 2:
                            excel_items.append({'name': p_name, 'qty': qty, 'value': val})
                    except Exception:
                        pass

        print(f"✅ Extracted from Downloaded Excel: {len(excel_items)} Products!")
        for item in excel_items[:10]:
            print(f"   • {item['name']} | Qty: {item['qty']} | Value: {item['value']}")
    else:
        print("❌ Excel download failed.")
