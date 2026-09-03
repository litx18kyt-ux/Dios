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

print("=== CBO SPO AUGUST 2026 NATIVE CAPTURE LOG ===\n")

CBO_USER = os.getenv("CBO_USER", "6958BANWARI")
CBO_PASS = os.getenv("CBO_PASS", "6958")
LOGIN_URL = "https://dios.myreporting.net/erp/login"

def run():
    print("🚀 [1/5] Launching Browser...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
        context = browser.new_context(viewport={"width": 1440, "height": 900}, accept_downloads=True)
        page = context.new_page()
        page.set_default_timeout(25000)

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

        # 2. Open Reports -> Sales & Targets -> SPO Stockist Wise
        print("🧭 [3/5] Navigating to SPO Stockist Wise...")
        page.locator("a:has-text('Reports'), span:has-text('Reports'), li:has-text('Reports')").first.click()
        page.wait_for_timeout(600)

        # Mouseover Sales & Targets
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

        # Click SPO Stockist Wise
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

        # 3. Native Physical Click on Green Filter Funnel (filter.svg)
        print("🔍 [4/5] Clicking Filter Funnel Icon with Native Mouse Click...")
        
        # Click the filter image or its parent anchor natively
        filter_icon = page.locator("img[src*='filter'], a:has(img[src*='filter'])").first
        if filter_icon.count() > 0:
            filter_icon.click(force=True)
            print("   ✅ Filter Funnel clicked via Native Locator!")
        else:
            print("   ⚠️ Fallback search for filter icon...")
            page.locator(".fa-filter, [title*='Filter']").first.click(force=True)

        page.wait_for_timeout(2500)

        # Inspect Modal Elements
        print("\n🔎 Inspecting Modal Dialog...")
        modal_info = page.evaluate('''() => {
            const isVis = el => el && (el.offsetWidth > 0 || el.offsetHeight > 0);
            const dialog = Array.from(document.querySelectorAll("div, .modal, .popup, [role='dialog'], .e-dialog")).find(d => isVis(d) && (d.innerText || '').includes('SPO Stockist Wise Report'));
            
            if (!dialog) return { found: false };

            const inputs = Array.from(dialog.querySelectorAll("input, select, textarea")).map(i => ({
                tag: i.tagName,
                type: i.type,
                id: i.id,
                name: i.name,
                value: i.value,
                placeholder: i.placeholder,
                className: i.className
            }));

            return { found: true, inputs: inputs };
        }''')
        print(f"   Modal Found: {modal_info['found']}")
        if modal_info['found']:
            print(f"   Inputs inside modal: {len(modal_info['inputs'])}")
            for idx, inp in enumerate(modal_info['inputs']):
                print(f"      [{idx}] <{inp['tag']} type='{inp['type']}'> id='{inp['id']}' val='{inp['value']}' ph='{inp['placeholder']}'")

        # 4. Fill Dates (From Date -> 01/08/2026, To Date -> 31/08/2026)
        print("\n📅 Injecting August 2026 Dates...")
        date_res = page.evaluate('''() => {
            const isVis = el => el && (el.offsetWidth > 0 || el.offsetHeight > 0);
            const dialog = Array.from(document.querySelectorAll("div, .modal, .popup, [role='dialog'], .e-dialog")).find(d => isVis(d) && (d.innerText || '').includes('SPO Stockist Wise Report'));
            const root = dialog || document.body;

            // Find all inputs in the dialog
            const inputs = Array.from(root.querySelectorAll("input")).filter(isVis);
            
            // From Date is input 0 or input with date value
            let fromInp = inputs.find(i => (i.value || '').includes('/'));
            let toInp = inputs.find(i => i !== fromInp && (i.value || '').includes('/'));

            if (!fromInp && inputs.length >= 2) {
                fromInp = inputs[0];
                toInp = inputs[1];
            }

            if (fromInp && toInp) {
                fromInp.value = "01/08/2026";
                fromInp.dispatchEvent(new Event('input', {bubbles: true}));
                fromInp.dispatchEvent(new Event('change', {bubbles: true}));

                toInp.value = "31/08/2026";
                toInp.dispatchEvent(new Event('input', {bubbles: true}));
                toInp.dispatchEvent(new Event('change', {bubbles: true}));

                return "SUCCESS: Set From=" + fromInp.value + " To=" + toInp.value;
            }

            return "FAILED: Inputs count = " + inputs.length;
        }''')
        print(f"   Status: {date_res}")

        # Also fill with Playwright native keyboard if possible
        try:
            date_pickers = page.locator("input:visible").filter(has_text="")
            for idx in range(min(date_pickers.count(), 2)):
                inp = date_pickers.nth(idx)
                curr_val = inp.get_attribute("value") or ""
                if "/" in curr_val:
                    new_val = "01/08/2026" if idx == 0 else "31/08/2026"
                    inp.fill(new_val)
                    print(f"   Playwright filled input {idx} with {new_val}")
        except Exception:
            pass

        # Click blue 'GO' button (Screenshot 3)
        print("\n🔘 Clicking GO button...")
        go_btn = page.locator("button:visible:has-text('GO'), input[value*='GO'], a:visible:has-text('GO')").first
        if go_btn.count() > 0:
            go_btn.click(force=True)
            print("   ✅ GO Button Clicked natively!")
        else:
            page.evaluate('''() => {
                const btns = Array.from(document.querySelectorAll("button, input[type='button'], a"));
                const b = btns.find(x => (x.innerText || x.value || '').trim().toUpperCase().includes('GO'));
                if (b) b.click();
            }''')
            print("   ✅ GO Button Clicked via JS!")

        print("⏳ Waiting 6 seconds for grid to reload with August data...")
        page.wait_for_timeout(6000)

        # 5. Download August Excel via Green Excel Icon (excel.png)
        print("📥 [5/5] Clicking Green Excel Icon (excel.png)...")
        aug_excel = "/workspaces/Dios/spo_august_verified.xls"

        with page.expect_download(timeout=20000) as dl_info:
            excel_icon = page.locator("img[src*='excel'], a:has(img[src*='excel'])").first
            if excel_icon.count() > 0:
                excel_icon.click(force=True)
            else:
                page.evaluate('''() => {
                    const elms = Array.from(document.querySelectorAll("a, button, img"));
                    const b = elms.find(e => (e.src || '').includes('excel') || (e.className || '').includes('excel') || (e.getAttribute('title') || '').toLowerCase().includes('excel'));
                    if (b) b.click();
                }''')
        
        dl = dl_info.value
        dl.save_as(aug_excel)
        print(f"🎉 Excel Saved: {aug_excel} ({os.path.getsize(aug_excel)} bytes)")

        browser.close()

    # 6. Parse and Print the Final Numbers
    print("\n" + "="*65)
    print("📊 PARSING AUGUST 2026 EXCEL DATA")
    print("="*65)

    if os.path.exists(aug_excel):
        aug_xlsx = "/workspaces/Dios/spo_august_verified.xlsx"
        shutil.copyfile(aug_excel, aug_xlsx)

        import openpyxl
        wb = openpyxl.load_workbook(aug_xlsx, data_only=True)
        ws = wb.active

        rows = list(ws.iter_rows(values_only=True))
        date_header = str(rows[2][0] if len(rows) > 2 else "")
        print(f"📅 Excel Header: {date_header[:80]}...\n")

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

    print("\n🏁 Done! All results written to: spo_test_output.txt")

if __name__ == "__main__":
    run()
