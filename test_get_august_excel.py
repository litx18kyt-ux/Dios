import os
import sys
import time
import shutil
import traceback
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

print("=== CBO SPO FINAL AUGUST EXCEL RETRIEVAL ENGINE ===\n")

CBO_USER = os.getenv("CBO_USER", "6958BANWARI")
CBO_PASS = os.getenv("CBO_PASS", "6958")
LOGIN_URL = "https://dios.myreporting.net/erp/login"

def run():
    print("🚀 [1/5] Launching Playwright Engine...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
        context = browser.new_context(viewport={"width": 1440, "height": 900}, accept_downloads=True)
        page = context.new_page()
        page.set_default_timeout(35000)
        page.on("dialog", lambda d: d.accept())

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
        page.locator("a:has-text('Reports'), span:has-text('Reports')").first.click()
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

        # 3. Open Modal via Funnel icon
        print("🔍 [4/5] Opening Filter Modal...")
        page.evaluate('''() => {
            const isVis = el => el && (el.offsetWidth > 0 || el.offsetHeight > 0);
            const all = Array.from(document.querySelectorAll('*'));
            const totalRecEl = all.find(e => (e.innerText || '').includes('Total Records') && e.children.length === 0);
            let container = totalRecEl ? totalRecEl.parentElement : document.body;
            for (let i = 0; i < 5; i++) {
                if (!container) break;
                const funnelImg = container.querySelector("img[src*='filter'], .filter, [title*='Filter']");
                if (funnelImg) {
                    funnelImg.click();
                    return;
                }
                container = container.parentElement;
            }
            const imgs = Array.from(document.querySelectorAll("img[src*='filter']")).filter(isVis);
            if (imgs.length > 0) imgs[imgs.length - 1].click();
        }''')
        page.wait_for_timeout(2500)

        # 4. Universal Date Injection (Both Syncfusion Instances + Direct Inputs)
        print("📅 Setting August Dates (01/08/2026 to 31/08/2026)...")
        date_res = page.evaluate('''() => {
            let logMsg = [];
            
            // Method 1: Syncfusion ej2_instances across entire page & modal
            const allEj2 = Array.from(document.querySelectorAll('*')).filter(e => e.ej2_instances && e.ej2_instances[0]);
            let pickers = allEj2.filter(e => {
                const mod = (e.ej2_instances[0].getModuleName ? e.ej2_instances[0].getModuleName() : '').toLowerCase();
                return mod.includes('date') || mod.includes('picker');
            });

            if (pickers.length >= 2) {
                const dFrom = new Date(2026, 7, 1);   // Aug 1, 2026
                const dTo = new Date(2026, 7, 31);   // Aug 31, 2026

                pickers[0].ej2_instances[0].value = dFrom;
                if (pickers[0].ej2_instances[0].dataBind) pickers[0].ej2_instances[0].dataBind();

                pickers[1].ej2_instances[0].value = dTo;
                if (pickers[1].ej2_instances[0].dataBind) pickers[1].ej2_instances[0].dataBind();
                logMsg.push("Updated " + pickers.length + " Syncfusion DatePicker instances!");
            }

            // Method 2: All inputs (including hidden/wrapped by Syncfusion)
            const allInputs = Array.from(document.querySelectorAll('input'));
            
            // Target inputs that have date values, date classes, or date IDs
            allInputs.forEach(i => {
                const val = (i.value || '');
                const id = (i.id || '').toLowerCase();
                const name = (i.name || '').toLowerCase();
                const cls = (i.className || '').toLowerCase();
                
                if (val.includes('01/09') || id.includes('from') || name.includes('from') || (cls.includes('date') && !id.includes('to'))) {
                    i.value = "01/08/2026";
                    i.dispatchEvent(new Event('input', { bubbles: true }));
                    i.dispatchEvent(new Event('change', { bubbles: true }));
                    i.dispatchEvent(new Event('blur', { bubbles: true }));
                    logMsg.push("Set From Date Input: " + i.id + " -> 01/08/2026");
                }
                if (val.includes('03/09') || id.includes('to') || name.includes('to') || (cls.includes('date') && id.includes('to'))) {
                    i.value = "31/08/2026";
                    i.dispatchEvent(new Event('input', { bubbles: true }));
                    i.dispatchEvent(new Event('change', { bubbles: true }));
                    i.dispatchEvent(new Event('blur', { bubbles: true }));
                    logMsg.push("Set To Date Input: " + i.id + " -> 31/08/2026");
                }
            });

            return logMsg.length > 0 ? logMsg.join(" | ") : "No date inputs/instances matched";
        }''')
        print(f"   {date_res}")
        page.wait_for_timeout(500)

        # 5. Click verified #GO Button
        print("🔘 Clicking GO Button (Direct ID #GO + F4)...")
        page.evaluate('''() => {
            const goBtn = document.getElementById("GO") || document.querySelector("button#GO") || document.querySelector("cbo-buttongo button");
            if (goBtn) goBtn.click();
        }''')
        page.keyboard.press("F4")
        print("   ✅ #GO clicked & F4 pressed!")

        print("⏳ Waiting 8 seconds for August 2026 grid to reload...")
        page.wait_for_timeout(8000)

        # 6. Download August Excel
        print("📥 [5/5] Downloading August Excel...")
        aug_excel = "/workspaces/Dios/spo_august_FINAL.xls"

        with page.expect_download(timeout=25000) as dl_info:
            page.evaluate('''() => {
                const isVis = el => el && (el.offsetWidth > 0 || el.offsetHeight > 0);
                const all = Array.from(document.querySelectorAll('*'));
                const totalRecEl = all.find(e => (e.innerText || '').includes('Total Records') && e.children.length === 0);
                let container = totalRecEl ? totalRecEl.parentElement : document.body;
                for (let i = 0; i < 5; i++) {
                    if (!container) break;
                    const excelBtn = container.querySelector("img[src*='excel'], .excel, [title*='Excel'], .fa-file-excel");
                    if (excelBtn) {
                        excelBtn.click();
                        return;
                    }
                    container = container.parentElement;
                }
                const elms = Array.from(document.querySelectorAll("img[src*='excel'], [title*='Excel']")).filter(isVis);
                if (elms.length > 0) elms[elms.length - 1].click();
            }''')

        dl = dl_info.value
        dl.save_as(aug_excel)
        print(f"🎉 Excel Saved: {aug_excel} ({os.path.getsize(aug_excel)} bytes)")

        browser.close()

    # 7. Parse and Print the August Data
    print("\n" + "="*65)
    print("📊 PARSING AUGUST 2026 VERIFIED EXCEL DATA")
    print("="*65)

    if os.path.exists(aug_excel):
        aug_xlsx = "/workspaces/Dios/spo_august_FINAL.xlsx"
        shutil.copyfile(aug_excel, aug_xlsx)

        import openpyxl
        wb = openpyxl.load_workbook(aug_xlsx, data_only=True)
        ws = wb.active

        rows = list(ws.iter_rows(values_only=True))
        date_header = str(rows[2][0] if len(rows) > 2 else "")
        print(f"📅 Excel Date Range: {date_header[:80]}...\n")

        print(f"{'Stockist Name':<25} | {'Sales (₹)':<12} | {'Return (₹)':<12} | {'Expiry (₹)':<12} | {'Net Sales (₹)':<12}")
        print("-" * 80)

        for r in rows[6:]:
            if not r or not any(r):
                continue
            name = str(r[1] or r[0] or '').strip()
            if any(k in name.upper() for k in ['NAGDA', 'R.P', 'VARDHMAN', 'SUN', 'MODI', 'DWARIKA', 'TOTAL']):
                sales_amt = str(r[4] or '0').strip()
                goods_ret = str(r[5] or '0').strip()
                expiry_ret = str(r[9] or '0').strip()
                net_sales = str(r[14] or '0').strip()

                print(f"{name:<25} | {sales_amt:<12} | {goods_ret:<12} | {expiry_ret:<12} | {net_sales:<12}")

    print("\n🏁 Master Execution Complete! All output in: spo_test_output.txt")

if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        print(f"\n❌ Error:\n{traceback.format_exc()}")
