import os, sys, time, re, csv
from playwright.sync_api import sync_playwright

MONTH_TARGET = sys.argv[1] if len(sys.argv) > 1 else "Aug-2026"
FY_TARGET = sys.argv[2] if len(sys.argv) > 2 else "2026-2027"

CBO_USER = os.getenv("CBO_USER", "6958BANWARI")
CBO_PASS = os.getenv("CBO_PASS", "6958")

DIRECT_REPORT_URL = f"https://dios.myreporting.net/RPT/PerformanceReview.aspx?format=Primary%20Sales&wise=P&DOC_TYPE=SS&RPT_HEADER=Monthly%20Sales-Summary&CBOYN=Y&FY_YEAR={FY_TARGET}&COMPANY_CODE=DIOS&PA_ID=6958&DESIG_ID=1&DESIG=BE&PA_NAME=BANWARI%20LAL%20MEENA&HEAD_QTR=UDAIPUR&DIVISION_NAME=DIOS%20GROUP&FMCGYN=N&MENU_STYLE=NONE&ACTION_FROM=ANDROID&LOGIN_PA_ID=6958&LOGIN_COMPANY_ID=1"

print("==========================================================")
print(f"🤖 DIOS PRIMARY BOT: Fetching Report for [{MONTH_TARGET}]")
print("==========================================================")

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--disable-popup-blocking", "--no-sandbox", "--disable-web-security"]
    )
    context = browser.new_context(viewport={"width": 1440, "height": 900}, accept_downloads=True)
    page = context.new_page()

    try:
        # Step 1: Login
        print("🌐 1. Activating Session on CBO ERP...")
        page.goto("https://dios.myreporting.net/erp/login", timeout=60000)
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(1500)

        user_input = page.locator("input[type='text']:visible").first
        pass_input = page.locator("input[type='password']:visible").first

        user_input.fill(CBO_USER)
        pass_input.fill(CBO_PASS)

        login_btn = page.locator("button:visible:not([hidden]):has-text('Login'), input[type='submit']:visible, button.btn-success:visible").first
        if login_btn.count() > 0:
            login_btn.click()
        else:
            pass_input.press("Enter")

        page.wait_for_timeout(3500)
        print("✅ Session Authenticated!")

        # Step 2: Open Direct URL Form
        print("🚀 2. Opening Monthly Sales Form Directly...")
        page.goto(DIRECT_REPORT_URL, timeout=60000)
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(2000)

        # Step 3: Set From Month & To Month to Target Month (e.g. Aug-2026)
        print(f"📋 3. Setting From & To Month to [{MONTH_TARGET}]...")
        filter_status = page.evaluate("""(targetMonth) => {
            const selects = Array.from(document.querySelectorAll('select'));
            let fromText = 'Not Set';
            let toText = 'Not Set';

            // Find month selects
            const monthSels = selects.filter(s => Array.from(s.options).some(o => o.text.includes('2026') || o.text.includes('Aug') || o.text.includes('Apr')));

            if (monthSels.length >= 2) {
                // From Month
                const optFrom = Array.from(monthSels[0].options).find(o => o.text.includes(targetMonth));
                if (optFrom) {
                    monthSels[0].value = optFrom.value;
                    monthSels[0].dispatchEvent(new Event('change', { bubbles: true }));
                    fromText = optFrom.text;
                }

                // To Month
                const optTo = Array.from(monthSels[1].options).find(o => o.text.includes(targetMonth));
                if (optTo) {
                    monthSels[1].value = optTo.value;
                    monthSels[1].dispatchEvent(new Event('change', { bubbles: true }));
                    toText = optTo.text;
                }
            }

            return { from: fromText, to: toText, count: selects.length };
        }""", MONTH_TARGET)

        print(f"📆 From Month Set : {filter_status['from']}")
        print(f"📆 To Month Set   : {filter_status['to']}")

        # Step 4: Click the Blue [Go] Button
        print("⚡ 4. Clicking Blue [Go] Button...")
        os.makedirs("/workspaces/Dios/csv_output", exist_ok=True)
        out_excel = f"/workspaces/Dios/csv_output/Primary_{MONTH_TARGET}.xlsx"
        out_csv = f"/workspaces/Dios/csv_output/Primary_{MONTH_TARGET}.csv"

        go_btn = page.locator("button:has-text('Go'), a:has-text('Go'), input[value*='Go'], .btn-primary:has-text('Go')").first
        if go_btn.count() > 0:
            go_btn.click(force=True)
        else:
            page.evaluate("""() => {
                const all = Array.from(document.querySelectorAll('button, input, a'));
                const go = all.find(el => (el.textContent && el.textContent.trim().includes('Go')) || el.id === 'btnGo');
                if (go) go.click();
            }""")

        # Step 5: Wait for Report Page to Load
        print("⏳ 5. Waiting for Report Page to Render (6s)...")
        page.wait_for_timeout(6000)

        page.screenshot(path="/workspaces/Dios/csv_output/primary_report_generated.png")
        print(f"📄 Report Page Loaded! Title: {page.title() or 'PRIMARY SALES'}")

        # Step 6: Click Top-Right Blue [Excel] Button
        print("📥 6. Exporting Official Excel File...")
        try:
            excel_btn = page.locator("a:has-text('Excel'), button:has-text('Excel'), :text('Excel'), a[title*='Excel']").first
            if excel_btn.count() > 0:
                with page.expect_download(timeout=15000) as dl_info:
                    excel_btn.click(force=True)
                dl = dl_info.value
                dl.save_as(out_excel)
                print(f"🎉 SUCCESS: Primary Official Excel Saved: {out_excel}")
        except Exception as e:
            print(f"Excel export trigger note: {e}")

        # Step 7: Scrape Table directly from Report Page
        print("📊 7. Extracting Product Rows from Primary Report Table...")
        scraped_rows = []
        tables = page.locator("table").all()
        for t in tables:
            t_text = t.inner_text().upper()
            if "CALGYM" in t_text or "PRIMARY QTY" in t_text or "PRIMARY SALES" in t_text:
                rows = t.locator("tr").all()
                for r in rows:
                    cells = [c.inner_text().strip() for c in r.locator("th, td").all()]
                    if any(cells):
                        scraped_rows.append(cells)
                if len(scraped_rows) > 5:
                    break

        if len(scraped_rows) > 0:
            with open(out_csv, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerows(scraped_rows)
            print(f"🎉 SUCCESS: Primary Data CSV Saved: {out_csv} ({len(scraped_rows)} Rows)\n")

            print(f"| {'PRODUCT NAME':<35} | {'PRIMARY QTY':<12} | {'PRIMARY VALUE (₹)':<18} |")
            print("|" + "-"*37 + "|" + "-"*14 + "|" + "-"*20 + "|")
            for r in scraped_rows[1:20]:
                if len(r) >= 2:
                    p_name = r[0]
                    p_qty = r[1] if len(r) > 1 else "-"
                    p_val = r[2] if len(r) > 2 else "-"
                    print(f"| {p_name:<35} | {p_qty:<12} | {p_val:<18} |")
        else:
            print("⚠️ Table search: check screenshot at csv_output/primary_report_generated.png")

    except Exception as err:
        print(f"⚠️ Bot Execution Error: {err}")
        page.screenshot(path="/workspaces/Dios/csv_output/bot_debug.png")
    finally:
        browser.close()
