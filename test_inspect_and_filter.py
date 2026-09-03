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
    f.write("=== SPO EXCEL INSPECTION & DATE FILTER TEST ===\n\n")

# Inspect downloaded binary file type
OLD_FILE = "/workspaces/Dios/spo_stockist_wise_aug2026.xls"
if os.path.exists(OLD_FILE):
    log(f"📄 Checking file format of {OLD_FILE}...")
    with open(OLD_FILE, "rb") as f:
        magic = f.read(16)
    log(f"Header magic bytes: {magic[:8]}")

CBO_USER = os.getenv("CBO_USER", "6958BANWARI")
CBO_PASS = os.getenv("CBO_PASS", "6958")
LOGIN_URL = "https://dios.myreporting.net/erp/login"

def run_filter_test():
    log("\n🧪 [1/5] Launching Browser for Filter & Download...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
        context = browser.new_context(viewport={"width": 1440, "height": 900}, accept_downloads=True)
        page = context.new_page()
        page.set_default_timeout(20000)
        page.on("dialog", lambda d: d.accept())

        # Login
        log("🔑 [2/5] Logging into CBO...")
        page.goto(LOGIN_URL, timeout=60000, wait_until="domcontentloaded")
        page.wait_for_timeout(1000)
        page.fill("input[type='text']:visible", CBO_USER)
        page.fill("input[type='password']:visible", CBO_PASS)
        page.locator("button:visible:has-text('Login'), input[type='submit']:visible, .btn-success:visible").first.click()

        page.wait_for_url("**/dashboard/home**", timeout=45000)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1500)
        log("✅ Dashboard Loaded!")

        # Navigate to Reports -> Sales & Targets -> SPO Stockist Wise
        page.locator("a:has-text('Reports'), span:has-text('Reports'), li:has-text('Reports')").first.click()
        page.wait_for_timeout(600)

        page.evaluate('''() => {
            const elms = Array.from(document.querySelectorAll('a, span, li, td'));
            const st = elms.find(e => (e.innerText || '').trim() === 'Sales & Targets');
            if (st) {
                st.dispatchEvent(new MouseEvent('mouseover', {bubbles: true}));
                st.dispatchEvent(new MouseEvent('mouseenter', {bubbles: true}));
                st.click();
            }
        }''')
        page.wait_for_timeout(600)

        page.evaluate('''() => {
            const elms = Array.from(document.querySelectorAll('a, span, li, td'));
            const spo = elms.find(e => (e.innerText || '').trim().includes('SPO Stockist Wise'));
            if (spo) {
                spo.dispatchEvent(new MouseEvent('mouseover', {bubbles: true}));
                spo.click();
                if (spo.parentElement && spo.parentElement.tagName === 'A') spo.parentElement.click();
            }
        }''')
        page.wait_for_timeout(3500)
        log("✅ Reached SPO Stockist Wise page!")

        # Click the Green Filter Funnel Icon (filter.svg)
        log("🔍 [3/5] Clicking Green Filter Funnel Icon (filter.svg)...")
        page.evaluate('''() => {
            const imgs = Array.from(document.querySelectorAll("img, a, button, i"));
            const filterBtn = imgs.find(e => (e.src || '').includes('filter') || (e.className || '').includes('filter') || (e.getAttribute('title') || '').toLowerCase().includes('filter'));
            if (filterBtn) filterBtn.click();
        }''')
        page.wait_for_timeout(2000)

        # Handle Modal (Screenshot 3) - Standard JS without invalid :visible selector
        log("📅 [4/5] Injecting Dates: 01/08/2026 to 31/08/2026...")
        date_fill_res = page.evaluate('''() => {
            const isVisible = (el) => !!(el && (el.offsetWidth > 0 || el.offsetHeight > 0));
            
            // 1. Try Syncfusion datepicker instances first
            const allPickers = Array.from(document.querySelectorAll('*')).filter(e => e.ej2_instances && e.ej2_instances[0] && e.ej2_instances[0].getModuleName && e.ej2_instances[0].getModuleName() === 'datepicker');
            if (allPickers.length >= 2) {
                allPickers[0].ej2_instances[0].value = new Date(2026, 7, 1);
                if (allPickers[0].ej2_instances[0].dataBind) allPickers[0].ej2_instances[0].dataBind();
                allPickers[1].ej2_instances[0].value = new Date(2026, 7, 31);
                if (allPickers[1].ej2_instances[0].dataBind) allPickers[1].ej2_instances[0].dataBind();
                return "SUCCESS: Dates set via Syncfusion ej2_instances!";
            }

            // 2. Fallback: Native visible inputs
            const allInputs = Array.from(document.querySelectorAll("input")).filter(isVisible);
            const dateInputs = allInputs.filter(i => (i.value || '').includes('/') || (i.name || i.id || '').toLowerCase().includes('date') || (i.placeholder || '').toLowerCase().includes('date'));
            
            let fromInput = dateInputs.length >= 2 ? dateInputs[0] : allInputs[0];
            let toInput = dateInputs.length >= 2 ? dateInputs[1] : allInputs[1];

            if (fromInput && toInput) {
                fromInput.value = "01/08/2026";
                fromInput.dispatchEvent(new Event('input', {bubbles: true}));
                fromInput.dispatchEvent(new Event('change', {bubbles: true}));

                toInput.value = "31/08/2026";
                toInput.dispatchEvent(new Event('input', {bubbles: true}));
                toInput.dispatchEvent(new Event('change', {bubbles: true}));
                return "SUCCESS: Dates set via inputs From=" + fromInput.value + " To=" + toInput.value;
            }

            return "FAILED: Visible inputs found: " + allInputs.length;
        }''')
        log(f"Status: {date_fill_res}")
        page.wait_for_timeout(1000)

        # Click blue 'GO' button (Screenshot 3)
        log("🔘 Clicking GO button...")
        clicked_go = page.evaluate('''() => {
            const isVisible = (el) => !!(el && (el.offsetWidth > 0 || el.offsetHeight > 0));
            const btns = Array.from(document.querySelectorAll("button, input[type='button'], a")).filter(isVisible);
            const goBtn = btns.find(b => (b.innerText || b.value || '').trim().toUpperCase().includes('GO'));
            if (goBtn) {
                goBtn.click();
                return true;
            }
            return false;
        }''')
        log(f"GO Button Clicked: {clicked_go}")

        log("⏳ Waiting 6 seconds for grid to reload with August data...")
        page.wait_for_timeout(6000)

        # Scrape Table on Screen Directly (Screenshot 2)
        log("\n📊 [5/5] Scraping Reloaded Screen Table Data...")
        scraped_data = page.evaluate('''() => {
            const out = [];
            const trs = Array.from(document.querySelectorAll("tr"));
            for (let tr of trs) {
                const cells = Array.from(tr.querySelectorAll("td, th")).map(c => (c.innerText || '').trim().replace(/\\n/g, ' '));
                if (cells.length >= 4) out.push(cells);
            }
            return out;
        }''')

        log(f"Screen Table Rows: {len(scraped_data)}")
        for r in scraped_data:
            line = " | ".join(r)
            if any(k in line.upper() for k in ['NAGDA', 'R.P', 'VARDHMAN', 'SUN', 'MODI', 'DWARIKA', 'TOTAL']):
                log(f"   👉 {line}")

        # Download Fresh Filtered Excel via Green Excel Icon
        fresh_excel = "/workspaces/Dios/spo_august_filtered.xls"
        try:
            with page.expect_download(timeout=15000) as dl_info:
                page.evaluate('''() => {
                    const isVisible = (el) => !!(el && (el.offsetWidth > 0 || el.offsetHeight > 0));
                    const elms = Array.from(document.querySelectorAll("a, button, i, img")).filter(isVisible);
                    const excelBtn = elms.find(e => {
                        const cls = (e.className || '').toLowerCase();
                        const title = (e.getAttribute('title') || '').toLowerCase();
                        const src = (e.src || '').toLowerCase();
                        return cls.includes('excel') || title.includes('excel') || src.includes('excel') || cls.includes('fa-file-excel');
                    });
                    if (excelBtn) excelBtn.click();
                }''')
            download = dl_info.value
            download.save_as(fresh_excel)
            log(f"🎉 Fresh Filtered Excel Downloaded: {fresh_excel} ({os.path.getsize(fresh_excel)} bytes)")
        except Exception as de:
            log(f"Excel download note: {de}")

        browser.close()
        log("\n🏁 Done! All results written to: spo_test_output.txt")

if __name__ == "__main__":
    run_filter_test()
