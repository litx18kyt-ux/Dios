import os
import sys
import time
from playwright.sync_api import sync_playwright

LOG_FILE = "/workspaces/Dios/spo_test_output.txt"

def log(msg):
    timestamp = time.strftime("%H:%M:%S")
    full_msg = f"[{timestamp}] {msg}"
    print(full_msg)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(full_msg + "\n")

with open(LOG_FILE, "w", encoding="utf-8") as f:
    f.write("=== CBO SPO STOCKIST WISE SYNCHRONIZED ENGINE LOG ===\n\n")

CBO_USER = os.getenv("CBO_USER", "6958BANWARI")
CBO_PASS = os.getenv("CBO_PASS", "6958")
LOGIN_URL = "https://dios.myreporting.net/erp/login"

def run():
    log("🚀 [1/6] Launching Chromium Engine...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
        context = browser.new_context(viewport={"width": 1440, "height": 900}, accept_downloads=True)
        page = context.new_page()
        page.set_default_timeout(15000)
        page.on("dialog", lambda d: d.accept())

        # 1. Login & Wait specifically for Angular Dashboard to load
        log("🔑 [2/6] Logging in to CBO Portal...")
        page.goto(LOGIN_URL, timeout=60000, wait_until="domcontentloaded")
        page.wait_for_timeout(1000)
        page.fill("input[type='text']:visible", CBO_USER)
        page.fill("input[type='password']:visible", CBO_PASS)
        page.locator("button:visible:has-text('Login'), input[type='submit']:visible, .btn-success:visible").first.click()

        log("⏳ Waiting for Angular Dashboard to finish loading...")
        page.wait_for_url("**/dashboard/home**", timeout=45000)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)
        log(f"✅ Dashboard is READY! Current URL: {page.url}")

        # 2. Open Reports -> Sales & Targets -> SPO Stockist Wise
        log("🧭 [3/6] Clicking Reports -> Sales & Targets -> SPO Stockist Wise...")
        
        # Click Reports in navbar
        reports_btn = page.locator("a:has-text('Reports'), span:has-text('Reports'), li:has-text('Reports')").first
        reports_btn.click()
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
        page.wait_for_timeout(800)

        # Click SPO Stockist Wise
        clicked_spo = page.evaluate('''() => {
            const elms = Array.from(document.querySelectorAll('a, span, li, td'));
            const spo = elms.find(e => (e.innerText || '').trim().includes('SPO Stockist Wise'));
            if (spo) {
                spo.dispatchEvent(new MouseEvent('mouseover', {bubbles: true}));
                spo.click();
                if (spo.parentElement && spo.parentElement.tagName === 'A') {
                    spo.parentElement.click();
                }
                return true;
            }
            return false;
        }''')
        log(f"Menu item clicked: {clicked_spo}")
        page.wait_for_timeout(3000)

        # 3. Handle Filter Dialog (Screenshot 3)
        log("📅 [4/6] Handling Filter Dialog & Setting Dates (01/08/2026 to 31/08/2026)...")
        
        # Check if dialog is open, if not click the green funnel icon
        page.evaluate('''() => {
            const isVis = el => el && (el.offsetWidth > 0 || el.offsetHeight > 0);
            const dialog = document.querySelector(".modal, .popup, [role='dialog'], .e-dialog");
            if (!dialog || !isVis(dialog)) {
                const icons = Array.from(document.querySelectorAll("a, button, i, span, img"));
                const funnel = icons.find(e => isVis(e) && ((e.className || '').includes('filter') || (e.getAttribute('title') || '').toLowerCase().includes('filter') || (e.src || '').includes('filter')));
                if (funnel) funnel.click();
            }
        }''')
        page.wait_for_timeout(1500)

        # Inject Dates (Supports both Syncfusion and native inputs)
        date_res = page.evaluate('''() => {
            // 1. Syncfusion Pickers
            const allElements = Array.from(document.querySelectorAll('*')).filter(e => e.ej2_instances && e.ej2_instances.length > 0);
            const pickers = allElements.filter(e => e.ej2_instances[0].getModuleName && e.ej2_instances[0].getModuleName() === 'datepicker');
            if (pickers.length >= 2) {
                pickers[0].ej2_instances[0].value = new Date(2026, 7, 1);
                if (pickers[0].ej2_instances[0].dataBind) pickers[0].ej2_instances[0].dataBind();
                pickers[1].ej2_instances[0].value = new Date(2026, 7, 31);
                if (pickers[1].ej2_instances[0].dataBind) pickers[1].ej2_instances[0].dataBind();
                return "SUCCESS via ej2_instances";
            }

            // 2. Input elements inside modal
            const isVis = el => el && (el.offsetWidth > 0 || el.offsetHeight > 0);
            const inputs = Array.from(document.querySelectorAll("input")).filter(isVis);
            const dInps = inputs.filter(i => (i.value || '').includes('/') || (i.placeholder || i.name || i.id || '').toLowerCase().includes('date'));
            if (dInps.length >= 2) {
                dInps[0].value = "01/08/2026";
                dInps[0].dispatchEvent(new Event('input', {bubbles: true}));
                dInps[0].dispatchEvent(new Event('change', {bubbles: true}));

                dInps[1].value = "31/08/2026";
                dInps[1].dispatchEvent(new Event('input', {bubbles: true}));
                dInps[1].dispatchEvent(new Event('change', {bubbles: true}));
                return "SUCCESS via date input fields";
            }
            return "Visible inputs count: " + inputs.length;
        }''')
        log(f"Date Injection: {date_res}")

        # Click blue 'GO' button (Screenshot 3)
        log("🔘 Clicking GO button...")
        clicked_go = page.evaluate('''() => {
            const isVis = el => el && (el.offsetWidth > 0 || el.offsetHeight > 0);
            const btns = Array.from(document.querySelectorAll("button, input[type='button'], a")).filter(isVis);
            const goBtn = btns.find(b => (b.innerText || b.value || '').trim().toUpperCase().includes('GO'));
            if (goBtn) { goBtn.click(); return true; }
            return false;
        }''')
        log(f"GO Button Clicked: {clicked_go}")

        log("⏳ Waiting 6 seconds for grid to load data...")
        page.wait_for_timeout(6000)

        # 4. Angle A: Direct Screen Table Scrape (Screenshot 2)
        log("\n📊 [5/6] Scraping Stockist Wise Data Directly from Screen...")
        table_data = page.evaluate('''() => {
            const results = [];
            const trs = Array.from(document.querySelectorAll("tr"));
            for (let tr of trs) {
                const cells = Array.from(tr.querySelectorAll("td, th")).map(c => (c.innerText || '').trim().replace(/\\n/g, ' '));
                if (cells.length >= 4) results.push(cells);
            }
            return results;
        }''')

        log(f"Found {len(table_data)} total table rows:")
        data_rows = []
        for r in table_data:
            line_str = " | ".join(r)
            if any(k in line_str.upper() for k in ['NAGDA', 'R.P', 'VARDHMAN', 'SUN', 'MODI', 'DWARIKA', 'TOTAL']):
                data_rows.append(r)
                log(f"   👉 {line_str}")

        # 5. Angle B: Excel File Download via Green Excel Icon
        log("\n📥 [6/6] Triggering Green Excel Download Icon...")
        output_file = "/workspaces/Dios/spo_stockist_wise_aug2026.xls"
        try:
            with page.expect_download(timeout=15000) as dl_info:
                clicked_excel = page.evaluate('''() => {
                    const isVis = el => el && (el.offsetWidth > 0 || el.offsetHeight > 0);
                    const elms = Array.from(document.querySelectorAll("a, button, i, img, span")).filter(isVis);
                    const excelBtn = elms.find(e => {
                        const cls = (e.className || '').toLowerCase();
                        const title = (e.getAttribute('title') || '').toLowerCase();
                        const src = (e.src || '').toLowerCase();
                        return cls.includes('excel') || title.includes('excel') || src.includes('excel') || cls.includes('fa-file-excel');
                    });
                    if (excelBtn) { excelBtn.click(); return true; }
                    return false;
                }''')
                log(f"Excel Export Icon Clicked: {clicked_excel}")

            download = dl_info.value
            download.save_as(output_file)
            size = os.path.getsize(output_file)
            log(f"🎉 EXCEL DOWNLOAD SUCCESSFUL! File saved to: {output_file} ({size} bytes)")
        except Exception as dle:
            log(f"Excel download timed out/skipped ({dle}). Scraped data is still available above!")

        browser.close()
        log("\n🏁 Engine run complete! All results saved in: spo_test_output.txt")

if __name__ == "__main__":
    run()
