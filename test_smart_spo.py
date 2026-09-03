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

print("=== CBO SPO SMART MODAL & AUGUST DATA ENGINE LOG ===\n")

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

        # 3. Check if Modal is already open (avoid closing it!)
        print("🔎 [4/5] Checking Filter Modal status...")
        is_already_open = page.evaluate('''() => {
            const isVis = el => el && (el.offsetWidth > 0 || el.offsetHeight > 0);
            const dialogs = Array.from(document.querySelectorAll("div, .modal, .popup, [role='dialog'], .e-dialog")).filter(isVis);
            return dialogs.some(d => (d.innerText || '').includes('SPO Stockist Wise Report') && (d.innerText || '').includes('From Date'));
        }''')

        if is_already_open:
            print("   🌟 Modal is ALREADY OPEN! (Skipping funnel icon to avoid closing it)")
        else:
            print("   Modal is not open yet, clicking Green Filter Funnel icon...")
            page.locator("img[src*='filter'], a:has(img[src*='filter'])").first.click(force=True)
            page.wait_for_timeout(2000)

        # 4. Fill Dates (From Date -> 01/08/2026, To Date -> 31/08/2026)
        print("📅 Setting August 2026 Dates in Modal...")
        date_fill_res = page.evaluate('''() => {
            const isVis = el => el && (el.offsetWidth > 0 || el.offsetHeight > 0);
            const dialog = Array.from(document.querySelectorAll("div, .modal, .popup, [role='dialog'], .e-dialog")).filter(isVis).find(d => (d.innerText || '').includes('SPO Stockist Wise Report') && (d.innerText || '').includes('From Date'));
            
            if (!dialog) return "ERROR: Modal Dialog not found in DOM!";

            const inputs = Array.from(dialog.querySelectorAll("input"));
            if (inputs.length >= 2) {
                inputs[0].value = "01/08/2026";
                inputs[0].dispatchEvent(new Event('input', {bubbles: true}));
                inputs[0].dispatchEvent(new Event('change', {bubbles: true}));

                inputs[1].value = "31/08/2026";
                inputs[1].dispatchEvent(new Event('input', {bubbles: true}));
                inputs[1].dispatchEvent(new Event('change', {bubbles: true}));

                return "SUCCESS: Set From=" + inputs[0].value + " To=" + inputs[1].value;
            }
            return "ERROR: Inputs count = " + inputs.length;
        }''')
        print(f"   Date Result: {date_fill_res}")

        # Native Playwright fill backup
        try:
            modal_loc = page.locator("div:has-text('SPO Stockist Wise Report'):has-text('From Date')").last
            m_inps = modal_loc.locator("input:visible")
            if m_inps.count() >= 2:
                m_inps.nth(0).fill("01/08/2026")
                m_inps.nth(1).fill("31/08/2026")
                print("   ✅ Playwright native fill also applied!")
        except Exception:
            pass

        page.wait_for_timeout(1000)

        # Click blue 'GO' button (Screenshot 3)
        print("🔘 Clicking GO button...")
        clicked_go = page.evaluate('''() => {
            const isVis = el => el && (el.offsetWidth > 0 || el.offsetHeight > 0);
            const dialog = Array.from(document.querySelectorAll("div, .modal, .popup, [role='dialog'], .e-dialog")).filter(isVis).find(d => (d.innerText || '').includes('SPO Stockist Wise Report'));
            const root = dialog || document;
            const btns = Array.from(root.querySelectorAll("button, input[type='button'], a")).filter(isVis);
            const goBtn = btns.find(b => (b.innerText || b.value || '').trim().toUpperCase().includes('GO'));
            if (goBtn) {
                goBtn.click();
                return true;
            }
            return false;
        }''')
        print(f"   GO Click Status: {clicked_go}")

        print("⏳ Waiting 6 seconds for August 2026 grid to reload...")
        page.wait_for_timeout(6000)

        # 5. Download August Excel
        print("📥 [5/5] Downloading August Excel...")
        aug_excel = "/workspaces/Dios/spo_august_verified.xls"

        with page.expect_download(timeout=20000) as dl_info:
            page.locator("img[src*='excel'], a:has(img[src*='excel'])").first.click(force=True)

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
