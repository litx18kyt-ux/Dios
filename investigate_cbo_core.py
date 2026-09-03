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

print("=== CBO CORE ARCHITECTURE DEEP INVESTIGATION LOG ===\n")

CBO_USER = os.getenv("CBO_USER", "6958BANWARI")
CBO_PASS = os.getenv("CBO_PASS", "6958")
LOGIN_URL = "https://dios.myreporting.net/erp/login"

def run():
    print("🚀 [1/4] Launching Browser Engine...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
        context = browser.new_context(viewport={"width": 1440, "height": 900}, accept_downloads=True)
        page = context.new_page()
        page.set_default_timeout(30000)

        # 1. Login
        print("🔑 [2/4] Logging into CBO...")
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
        print("🧭 [3/4] Opening SPO Stockist Wise...")
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

        # Inspect the exact menu element before clicking
        menu_info = page.evaluate('''() => {
            const elms = Array.from(document.querySelectorAll('a, span, li, td'));
            const spo = elms.find(e => (e.innerText || '').trim().includes('SPO Stockist Wise'));
            if (spo) {
                const parentA = spo.closest('a');
                return {
                    text: spo.innerText,
                    tag: spo.tagName,
                    href: parentA ? parentA.href : spo.getAttribute('href'),
                    routerLink: spo.getAttribute('routerlink') || (parentA ? parentA.getAttribute('routerlink') : null),
                    onclick: spo.getAttribute('onclick') || (parentA ? parentA.getAttribute('onclick') : null)
                };
            }
            return null;
        }''')
        print(f"ℹ️ SPO Menu Item Route Info: {menu_info}")

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

        # 3. Deep Forensic Inspection of Active Elements & Libraries
        print("\n" + "="*65)
        print("🔬 [4/4] FORENSIC INSPECTION: WHAT LIBRARIES IS CBO USING?")
        print("="*65)

        core_info = page.evaluate('''() => {
            const isVis = el => el && (el.offsetWidth > 0 || el.offsetHeight > 0);
            
            // Check global JS libraries
            const hasJQuery = typeof window.$ !== 'undefined';
            const hasJQueryUI = hasJQuery && typeof window.$.datepicker !== 'undefined';
            const hasFlatpickr = typeof window.flatpickr !== 'undefined';
            const hasBootstrap = typeof window.bootstrap !== 'undefined';

            // Find all visible input fields on the screen
            const allInputs = Array.from(document.querySelectorAll('input')).filter(isVis);
            const inputDetails = allInputs.map((inp, idx) => {
                // Check all HTML attributes on this input
                const attrs = {};
                for (let attr of inp.attributes) {
                    attrs[attr.name] = attr.value;
                }
                
                // Check jQuery data attached
                let jqData = null;
                if (hasJQuery && window.$(inp).data) {
                    try {
                        jqData = Object.keys(window.$(inp).data());
                    } catch(e) {}
                }

                return {
                    index: idx,
                    id: inp.id,
                    name: inp.name,
                    type: inp.type,
                    value: inp.value,
                    placeholder: inp.placeholder,
                    className: inp.className,
                    attributes: attrs,
                    jqDataKeys: jqData
                };
            });

            // Find all buttons
            const allBtns = Array.from(document.querySelectorAll('button, input[type="button"], a')).filter(isVis).map(b => ({
                text: (b.innerText || b.value || '').trim(),
                id: b.id,
                className: b.className,
                type: b.type || ''
            }));

            return {
                libraries: {
                    jQuery: hasJQuery,
                    jQueryUIDatepicker: hasJQueryUI,
                    flatpickr: hasFlatpickr,
                    bootstrap: hasBootstrap
                },
                inputs: inputDetails,
                buttons: allBtns.filter(b => b.text.length > 0 && b.text.length < 30)
            };
        }''')

        print("📚 Global Libraries Detected:")
        print(f"   jQuery: {core_info['libraries']['jQuery']}")
        print(f"   jQuery UI Datepicker: {core_info['libraries']['jQueryUIDatepicker']}")
        print(f"   Flatpickr: {core_info['libraries']['flatpickr']}")

        print(f"\n📝 All Visible Inputs ({len(core_info['inputs'])}):")
        for inp in core_info['inputs']:
            print(f"\n   👉 Input [{inp['index']}]: id='{inp['id']}', name='{inp['name']}', type='{inp['type']}', val='{inp['value']}'")
            print(f"      Attributes: {inp['attributes']}")
            if inp['jqDataKeys']:
                print(f"      jQuery Data Keys: {inp['jqDataKeys']}")

        print(f"\n🔘 All Visible Buttons ({len(core_info['buttons'])}):")
        for btn in core_info['buttons']:
            print(f"   Button -> text='{btn['text']}', id='{btn['id']}', class='{btn['className']}'")

        # 4. Try Setting Dates directly via discovered properties
        print("\n" + "="*65)
        print("🎯 TESTING DIRECT PROPERTY / JQUERY DATE SETTING")
        print("="*65)

        date_change_test = page.evaluate('''() => {
            const isVis = el => el && (el.offsetWidth > 0 || el.offsetHeight > 0);
            const inputs = Array.from(document.querySelectorAll('input')).filter(isVis);
            
            let changed = 0;
            inputs.forEach(inp => {
                const val = inp.value || '';
                // If it looks like date (e.g. 01/09/2026 or 03/09/2026)
                if (val.includes('/2026') || val.includes('/09/')) {
                    const newVal = val.replace('/09/', '/08/');
                    
                    // If jQuery UI datepicker is attached
                    if (window.$ && window.$(inp).datepicker) {
                        try {
                            window.$(inp).datepicker("setDate", newVal);
                            changed++;
                            return;
                        } catch(e) {}
                    }

                    // Native setting
                    inp.value = newVal;
                    inp.dispatchEvent(new Event('input', { bubbles: true }));
                    inp.dispatchEvent(new Event('change', { bubbles: true }));
                    inp.dispatchEvent(new Event('blur', { bubbles: true }));
                    changed++;
                }
            });
            return "Attempted update on " + changed + " inputs";
        }''')
        print(f"Date Change Attempt: {date_change_test}")

        # Click GO if found
        print("🔘 Clicking GO button...")
        clicked_go = page.evaluate('''() => {
            const btns = Array.from(document.querySelectorAll('button, input[type="button"], a'));
            const goBtn = btns.find(b => (b.innerText || b.value || '').trim().toUpperCase() === 'GO');
            if (goBtn) {
                goBtn.click();
                return true;
            }
            return false;
        }''')
        print(f"GO Clicked: {clicked_go}")

        page.wait_for_timeout(6000)

        # 5. Intercept the Excel Download Event & Capture URL
        print("\n" + "="*65)
        print("📥 EXCEL DOWNLOAD & URL EXTRACTION")
        print("="*65)

        test_excel = "/workspaces/Dios/spo_investigated.xls"
        with page.expect_download(timeout=20000) as dl_info:
            page.evaluate('''() => {
                const elms = Array.from(document.querySelectorAll("a, button, i, span, img"));
                const excelBtn = elms.find(e => {
                    const src = (e.src || '').toLowerCase();
                    const cls = (e.className || '').toLowerCase();
                    const title = (e.getAttribute('title') || '').toLowerCase();
                    return src.includes('excel') || cls.includes('excel') || title.includes('excel') || cls.includes('fa-file-excel');
                });
                if (excelBtn) excelBtn.click();
            }''')

        download = dl_info.value
        print(f"🌟 ACTUAL DOWNLOAD URL: {download.url}")
        print(f"📁 SUGGESTED FILENAME: {download.suggested_filename}")

        download.save_as(test_excel)
        print(f"💾 File Saved ({os.path.getsize(test_excel)} bytes)")

        browser.close()

    # Parse Row 2 of the downloaded file
    if os.path.exists(test_excel):
        shutil.copyfile(test_excel, "/workspaces/Dios/spo_investigated.xlsx")
        import openpyxl
        wb = openpyxl.load_workbook("/workspaces/Dios/spo_investigated.xlsx", data_only=True)
        ws = wb.active
        rows = list(ws.iter_rows(values_only=True))
        if len(rows) > 2:
            print(f"\n📅 Downloaded Excel Row [2]: {rows[2][0]}")

    print("\n🏁 Investigation complete! Results in: spo_test_output.txt")

if __name__ == "__main__":
    run()
