import os
import sys
import time
import shutil
from playwright.sync_api import sync_playwright

LOG_FILE = "/workspaces/Dios/spo_test_output.txt"

class TeeLogger:
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.logfile = open(filename, "w", encoding="utf-8")

    def write(self, message):
        self.terminal.write(message)
        self.terminal.flush()
        self.logfile.write(message)
        self.logfile.flush()

    def flush(self):
        self.terminal.flush()
        self.logfile.flush()

sys.stdout = TeeLogger(LOG_FILE)
sys.stderr = sys.stdout

print("=== CBO SPO AUGUST 2026 NON-BLOCKING ENGINE LOG ===\n")

CBO_USER = os.getenv("CBO_USER", "6958BANWARI")
CBO_PASS = os.getenv("CBO_PASS", "6958")
LOGIN_URL = "https://dios.myreporting.net/erp/login"

def run():
    print("🚀 [1/5] Launching Browser...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
        context = browser.new_context(viewport={"width": 1440, "height": 900}, accept_downloads=True)
        page = context.new_page()
        page.set_default_timeout(15000)

        # 1. Login
        print("🔑 [2/5] Logging into CBO...")
        page.goto(LOGIN_URL, timeout=60000, wait_until="domcontentloaded")
        page.wait_for_timeout(1000)
        page.fill("input[type='text']:visible", CBO_USER)
        page.fill("input[type='password']:visible", CBO_PASS)
        page.locator("button:visible:has-text('Login'), input[type='submit']:visible, .btn-success:visible").first.click()

        page.wait_for_url("**/dashboard/home**", timeout=45000)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1500)
        print("✅ Dashboard Ready!")

        # 2. Navigate to SPO Stockist Wise
        print("🧭 [3/5] Navigating to SPO Stockist Wise...")
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

        # 3. Open Filter Modal via Green Funnel Icon
        print("🔍 [4/5] Opening Filter Dialog (filter.svg)...")
        page.evaluate('''() => {
            const imgs = Array.from(document.querySelectorAll("img, a, button, i"));
            const filterBtn = imgs.find(e => (e.src || '').includes('filter') || (e.className || '').includes('filter') || (e.getAttribute('title') || '').toLowerCase().includes('filter'));
            if (filterBtn) filterBtn.click();
        }''')
        page.wait_for_timeout(2000)

        # 4. Non-Blocking Date Filling (Bypasses Calendar Overlays)
        print("⌨️ Filling Dates without triggering calendar blocking...")
        
        modal = page.locator(".modal, .popup, [role='dialog'], .e-dialog, div:has-text('SPO Stockist Wise Report')").last
        inputs = modal.locator("input:visible")
        count = inputs.count()
        print(f"   Visible modal inputs: {count}")

        # Dump info of each input
        for idx in range(count):
            inp = inputs.nth(idx)
            val = inp.get_attribute("value") or ""
            ph = inp.get_attribute("placeholder") or ""
            name = inp.get_attribute("name") or inp.get_attribute("id") or ""
            print(f"   Input [{idx}]: Name='{name}', Placeholder='{ph}', Value='{val}'")

        # Safely fill From Date and To Date using .fill()
        try:
            from_inp = inputs.nth(0)
            to_inp = inputs.nth(1)

            from_inp.fill("01/08/2026")
            from_inp.dispatch_event("input")
            from_inp.dispatch_event("change")
            print("   ✅ Set From Date -> 01/08/2026")

            # Press Escape to ensure no calendar overlay is open
            page.keyboard.press("Escape")
            page.wait_for_timeout(300)

            to_inp.fill("31/08/2026")
            to_inp.dispatch_event("input")
            to_inp.dispatch_event("change")
            print("   ✅ Set To Date   -> 31/08/2026")

            page.keyboard.press("Escape")
            page.wait_for_timeout(300)

        except Exception as e:
            print(f"   Fill note: {e}")

        # Syncfusion fallback injection directly into JS instances
        sync_res = page.evaluate('''() => {
            const allElements = Array.from(document.querySelectorAll('*')).filter(e => e.ej2_instances && e.ej2_instances.length > 0);
            const pickers = allElements.filter(e => e.ej2_instances[0].getModuleName && e.ej2_instances[0].getModuleName() === 'datepicker');
            if (pickers.length >= 2) {
                pickers[0].ej2_instances[0].value = new Date(2026, 7, 1);
                if (pickers[0].ej2_instances[0].dataBind) pickers[0].ej2_instances[0].dataBind();

                pickers[1].ej2_instances[0].value = new Date(2026, 7, 31);
                if (pickers[1].ej2_instances[0].dataBind) pickers[1].ej2_instances[0].dataBind();
                return "Syncfusion instances updated directly!";
            }
            return "No ej2_instances needed.";
        }''')
        print(f"   Syncfusion status: {sync_res}")

        # Click blue 'GO' button (Screenshot 3)
        print("🔘 Clicking GO button...")
        go_btn = modal.locator("button:has-text('GO'), input[value*='GO'], a:has-text('GO')").first
        if go_btn.count() > 0:
            go_btn.click(force=True)
            print("   GO clicked via Playwright force click!")
        else:
            page.evaluate('''() => {
                const btns = Array.from(document.querySelectorAll("button, input[type='button'], a"));
                const b = btns.find(x => (x.innerText || x.value || '').trim().toUpperCase().includes('GO'));
                if (b) b.click();
            }''')
            print("   GO clicked via JS fallback!")

        print("⏳ Waiting 6 seconds for August 2026 data to load...")
        page.wait_for_timeout(6000)

        # 5. Download August Excel
        print("📥 [5/5] Downloading August Excel...")
        aug_excel = "/workspaces/Dios/spo_august_real.xls"
        try:
            with page.expect_download(timeout=20000) as dl_info:
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
            dl = dl_info.value
            dl.save_as(aug_excel)
            print(f"🎉 Excel Saved: {aug_excel} ({os.path.getsize(aug_excel)} bytes)")
        except Exception as dle:
            print(f"Excel download note: {dle}")

        browser.close()

    # 6. Parse and Print the Real August Numbers
    print("\n" + "="*65)
    print("📊 FINAL VERIFIED AUGUST 2026 PERFORMANCE NUMBERS")
    print("="*65)
    
    if os.path.exists(aug_excel):
        aug_xlsx = "/workspaces/Dios/spo_august_real.xlsx"
        shutil.copyfile(aug_excel, aug_xlsx)

        import openpyxl
        wb = openpyxl.load_workbook(aug_xlsx, data_only=True)
        ws = wb.active

        rows = list(ws.iter_rows(values_only=True))
        date_header = str(rows[2][0] if len(rows) > 2 else "")
        print(f"📅 Report Header Range: {date_header[:60]}...\n")

        print(f"{'Stockist Name':<25} | {'Sales (₹)':<12} | {'Return (₹)':<12} | {'Expiry (₹)':<12} | {'Net Sales (₹)':<12}")
        print("-" * 80)

        for r in rows[6:]:
            if not r or not any(r):
                continue
            stk_name = str(r[1] or '').strip()
            if not stk_name:
                stk_name = str(r[0] or '').strip()
            
            if any(k in stk_name.upper() for k in ['NAGDA', 'R.P', 'VARDHMAN', 'SUN', 'MODI', 'DWARIKA', 'TOTAL']):
                sales_amt = str(r[4] or '0').strip()
                goods_ret = str(r[5] or '0').strip()
                expiry_ret = str(r[9] or '0').strip()
                net_sales = str(r[14] or '0').strip()

                print(f"{stk_name:<25} | {sales_amt:<12} | {goods_ret:<12} | {expiry_ret:<12} | {net_sales:<12}")

    print("\n🏁 Done! Results written to: spo_test_output.txt")

if __name__ == "__main__":
    run()
