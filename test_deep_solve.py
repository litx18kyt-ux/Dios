import os
import sys
import time
import json
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

print("=== CBO SPO 1000-IQ LABEL-ANCHORED & API SNIFFER LOG ===\n")

CBO_USER = os.getenv("CBO_USER", "6958BANWARI")
CBO_PASS = os.getenv("CBO_PASS", "6958")
LOGIN_URL = "https://dios.myreporting.net/erp/login"

def run():
    print("🚀 [1/6] Launching Chromium Engine...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
        context = browser.new_context(viewport={"width": 1440, "height": 900}, accept_downloads=True)
        page = context.new_page()
        page.set_default_timeout(25000)

        # Network Sniffer
        api_responses = []
        def handle_response(res):
            if "apirequest" in res.url or "spo" in res.url.lower():
                try:
                    text = res.text()
                    api_responses.append({"url": res.url, "status": res.status, "body": text[:300]})
                except Exception:
                    pass
        page.on("response", handle_response)

        # 1. Login
        print("🔑 [2/6] Logging in to CBO...")
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
        print("🧭 [3/6] Navigating to SPO Stockist Wise...")
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

        # 3. Open Filter Modal
        print("🔍 [4/6] Opening Filter Modal (filter.svg)...")
        page.evaluate('''() => {
            const isVis = el => el && (el.offsetWidth > 0 || el.offsetHeight > 0);
            const dialog = document.querySelector(".modal, .popup, [role='dialog'], .e-dialog");
            if (!dialog || !isVis(dialog)) {
                const imgs = Array.from(document.querySelectorAll("img, a, button, i")).filter(isVis);
                const filterBtn = imgs.find(e => (e.src || '').includes('filter') || (e.className || '').includes('filter') || (e.getAttribute('title') || '').toLowerCase().includes('filter'));
                if (filterBtn) filterBtn.click();
            }
        }''')
        page.wait_for_timeout(2000)

        # 4. Label-Anchored Date Injection
        print("📅 [5/6] Injecting August 2026 Dates via Label Anchors...")
        date_probe = page.evaluate('''() => {
            const isVis = el => el && (el.offsetWidth > 0 || el.offsetHeight > 0);
            const allElements = Array.from(document.querySelectorAll('*'));
            
            // Find labels
            const fromLabel = allElements.find(e => (e.innerText || '').trim().startsWith('From Date'));
            const toLabel = allElements.find(e => (e.innerText || '').trim().startsWith('To Date'));

            let fromInp = null;
            let toInp = null;

            if (fromLabel && fromLabel.parentElement) {
                fromInp = fromLabel.parentElement.querySelector('input');
                if (!fromInp && fromLabel.parentElement.parentElement) {
                    fromInp = fromLabel.parentElement.parentElement.querySelector('input');
                }
            }

            if (toLabel && toLabel.parentElement) {
                toInp = toLabel.parentElement.querySelector('input');
                if (!toInp && toLabel.parentElement.parentElement) {
                    toInp = toLabel.parentElement.parentElement.querySelector('input');
                }
            }

            // If not found by hierarchy, find input immediately preceding or following
            const inputs = Array.from(document.querySelectorAll('input')).filter(isVis);
            
            return {
                fromFound: !!fromInp,
                toFound: !!toInp,
                fromTag: fromInp ? fromInp.tagName : null,
                fromType: fromInp ? fromInp.type : null,
                fromVal: fromInp ? fromInp.value : null,
                fromId: fromInp ? fromInp.id : null,
                fromHTML: fromInp ? fromInp.outerHTML.substring(0, 150) : null,
                toTag: toInp ? toInp.tagName : null,
                toType: toInp ? toInp.type : null,
                toVal: toInp ? toInp.value : null,
                toId: toInp ? toInp.id : null,
                toHTML: toInp ? toInp.outerHTML.substring(0, 150) : null,
                allVisibleInputsCount: inputs.length
            };
        }''')
        print(f"   From Input Detected: {date_probe['fromFound']} (Type: {date_probe['fromType']}, Val: {date_probe['fromVal']}, ID: {date_probe['fromId']})")
        print(f"   To Input Detected:   {date_probe['toFound']} (Type: {date_probe['toType']}, Val: {date_probe['toVal']}, ID: {date_probe['toId']})")

        # Now fill them with both formats
        fill_status = page.evaluate('''() => {
            const allElements = Array.from(document.querySelectorAll('*'));
            const fromLabel = allElements.find(e => (e.innerText || '').trim().startsWith('From Date'));
            const toLabel = allElements.find(e => (e.innerText || '').trim().startsWith('To Date'));

            let fInp = fromLabel && fromLabel.parentElement ? (fromLabel.parentElement.querySelector('input') || fromLabel.parentElement.parentElement.querySelector('input')) : null;
            let tInp = toLabel && toLabel.parentElement ? (toLabel.parentElement.querySelector('input') || toLabel.parentElement.parentElement.querySelector('input')) : null;

            if (!fInp || !tInp) {
                // Fallback by date values or date pickers
                const inputs = Array.from(document.querySelectorAll('input'));
                fInp = inputs.find(i => (i.value || '').includes('2026') || (i.id || '').toLowerCase().includes('from'));
                tInp = inputs.find(i => i !== fInp && ((i.value || '').includes('2026') || (i.id || '').toLowerCase().includes('to')));
            }

            if (fInp && tInp) {
                // Format for date type vs text type
                const fromVal = (fInp.type === 'date') ? '2026-08-01' : '01/08/2026';
                const toVal = (tInp.type === 'date') ? '2026-08-31' : '31/08/2026';

                fInp.value = fromVal;
                fInp.dispatchEvent(new Event('input', {bubbles: true}));
                fInp.dispatchEvent(new Event('change', {bubbles: true}));

                tInp.value = toVal;
                tInp.dispatchEvent(new Event('input', {bubbles: true}));
                tInp.dispatchEvent(new Event('change', {bubbles: true}));

                return "SUCCESS: Set From=" + fromVal + " and To=" + toVal;
            }

            return "FAILED to locate inputs via labels";
        }''')
        print(f"   Date Fill Execution: {fill_status}")
        page.wait_for_timeout(1000)

        # Click blue 'GO' button (Screenshot 3)
        print("🔘 Clicking GO button...")
        clicked_go = page.evaluate('''() => {
            const isVis = el => el && (el.offsetWidth > 0 || el.offsetHeight > 0);
            const btns = Array.from(document.querySelectorAll("button, input[type='button'], a")).filter(isVis);
            const go = btns.find(b => (b.innerText || b.value || '').trim().toUpperCase().includes('GO'));
            if (go) {
                go.click();
                return true;
            }
            return false;
        }''')
        print(f"   GO Click Status: {clicked_go}")

        print("⏳ Waiting 6 seconds for table to reload with August data...")
        page.wait_for_timeout(6000)

        # 5. Download August Excel
        print("📥 [6/6] Downloading August Excel...")
        aug_excel = "/workspaces/Dios/spo_august_verified.xls"
        try:
            with page.expect_download(timeout=20000) as dl_info:
                page.evaluate('''() => {
                    const isVis = el => el && (el.offsetWidth > 0 || el.offsetHeight > 0);
                    const elms = Array.from(document.querySelectorAll("a, button, i, img")).filter(isVis);
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
            print(f"🎉 Downloaded File: {aug_excel} ({os.path.getsize(aug_excel)} bytes)")
        except Exception as de:
            print(f"Download note: {de}")

        browser.close()

    # 6. Parse and Print the Final August Data
    print("\n" + "="*65)
    print("📊 FINAL AUGUST 2026 VERIFIED NUMBERS")
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

    print(f"\nCaptured {len(api_responses)} background responses.")
    for res in api_responses[-3:]:
        print(f"   API: {res['url']} (Status: {res['status']}) -> {res['body'][:100]}")

    print("\n🏁 Done! Results written to: spo_test_output.txt")

if __name__ == "__main__":
    run()
