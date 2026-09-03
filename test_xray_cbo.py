import os
import sys
import time
import json
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

print("=== CBO SPO 1000-IQ DEEP X-RAY & API SPY LOG ===\n")

CBO_USER = os.getenv("CBO_USER", "6958BANWARI")
CBO_PASS = os.getenv("CBO_PASS", "6958")
LOGIN_URL = "https://dios.myreporting.net/erp/login"

def run_xray():
    print("🚀 Launching Engine with Network Interceptor...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
        context = browser.new_context(viewport={"width": 1440, "height": 900}, accept_downloads=True)
        page = context.new_page()
        page.set_default_timeout(20000)

        # Network Spy: Intercept all CBO API payloads
        captured_payloads = []
        def handle_request(req):
            if "apirequest" in req.url or "spo" in req.url.lower() or "report" in req.url.lower():
                try:
                    p_data = req.post_data
                    captured_payloads.append({"url": req.url, "post_data": p_data})
                except Exception:
                    pass
        page.on("request", handle_request)

        # 1. Login
        print("🔑 Logging into CBO...")
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
        print("🧭 Opening Reports -> Sales & Targets -> SPO Stockist Wise...")
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
        print("🔍 Clicking Filter Funnel Icon (filter.svg)...")
        page.evaluate('''() => {
            const imgs = Array.from(document.querySelectorAll("img, a, button, i"));
            const filterBtn = imgs.find(e => (e.src || '').includes('filter') || (e.className || '').includes('filter') || (e.getAttribute('title') || '').toLowerCase().includes('filter'));
            if (filterBtn) filterBtn.click();
        }''')
        page.wait_for_timeout(2000)

        # 4. DEEP X-RAY: Find elements containing current date '01/09/2026' or '03/09/2026'
        print("\n" + "="*65)
        print("🔬 DEEP X-RAY: HUNTING FOR DATEPICKER ELEMENTS")
        print("="*65)

        xray_results = page.evaluate('''() => {
            const found = [];
            const allElements = Array.from(document.querySelectorAll('*'));
            
            allElements.forEach(el => {
                const val = (el.value || '').toString().trim();
                const text = (el.innerText || el.textContent || '').trim();
                
                // Match 01/09/2026 or 03/09/2026
                if (val.includes('01/09') || val.includes('03/09') || text === '01/09/2026' || text === '03/09/2026') {
                    found.push({
                        tag: el.tagName,
                        id: el.id,
                        name: el.getAttribute('name'),
                        className: el.className,
                        type: el.getAttribute('type'),
                        value: val,
                        text: text,
                        outerHTML: el.outerHTML.substring(0, 250),
                        parentTag: el.parentElement ? el.parentElement.tagName : null,
                        parentHTML: el.parentElement ? el.parentElement.outerHTML.substring(0, 250) : null
                    });
                }
            });

            // Also find elements near "From Date" label
            const fromLabel = allElements.find(e => (e.innerText || '').trim().startsWith('From Date'));
            const toLabel = allElements.find(e => (e.innerText || '').trim().startsWith('To Date'));

            return {
                matchedDates: found,
                fromLabelParent: fromLabel && fromLabel.parentElement ? fromLabel.parentElement.outerHTML.substring(0, 350) : null,
                toLabelParent: toLabel && toLabel.parentElement ? toLabel.parentElement.outerHTML.substring(0, 350) : null
            };
        }''')

        print(f"Elements found holding current dates: {len(xray_results['matchedDates'])}")
        for idx, item in enumerate(xray_results['matchedDates']):
            print(f"\n👉 Match [{idx}]: <{item['tag']}> id='{item['id']}' name='{item['name']}' class='{item['className']}' value='{item['value']}' text='{item['text']}'")
            print(f"   HTML: {item['outerHTML']}")

        if xray_results['fromLabelParent']:
            print(f"\n🏷️ 'From Date' Container HTML:\n{xray_results['fromLabelParent']}")
        if xray_results['toLabelParent']:
            print(f"\n🏷️ 'To Date' Container HTML:\n{xray_results['toLabelParent']}")

        # 5. Injection: Set dates directly on matched elements
        print("\n" + "="*65)
        print("🎯 ATTEMPTING SMART DATE INJECTION (01/08/2026 to 31/08/2026)")
        print("="*65)

        inject_res = page.evaluate('''() => {
            const allElements = Array.from(document.querySelectorAll('*'));
            const fromEls = allElements.filter(e => (e.value && e.value.includes('01/09')) || ((e.innerText || '').trim() === '01/09/2026'));
            const toEls = allElements.filter(e => (e.value && e.value.includes('03/09')) || ((e.innerText || '').trim() === '03/09/2026'));

            let count = 0;
            fromEls.forEach(el => {
                if (el.tagName === 'INPUT') {
                    el.value = "01/08/2026";
                    el.dispatchEvent(new Event('input', {bubbles: true}));
                    el.dispatchEvent(new Event('change', {bubbles: true}));
                    count++;
                } else {
                    el.innerText = "01/08/2026";
                    count++;
                }
            });

            toEls.forEach(el => {
                if (el.tagName === 'INPUT') {
                    el.value = "31/08/2026";
                    el.dispatchEvent(new Event('input', {bubbles: true}));
                    el.dispatchEvent(new Event('change', {bubbles: true}));
                    count++;
                } else {
                    el.innerText = "31/08/2026";
                    count++;
                }
            });

            return "Modified " + count + " date elements directly!";
        }''')
        print(f"Injection Status: {inject_res}")

        # Click GO Button
        print("\n🔘 Clicking GO Button...")
        page.evaluate('''() => {
            const isVisible = (el) => !!(el && (el.offsetWidth > 0 || el.offsetHeight > 0));
            const btns = Array.from(document.querySelectorAll("button, input[type='button'], a")).filter(isVisible);
            const go = btns.find(b => (b.innerText || b.value || '').trim().toUpperCase().includes('GO'));
            if (go) go.click();
        }''')
        page.wait_for_timeout(6000)

        # Check Intercepted API calls
        print("\n" + "="*65)
        print("📡 INTERCEPTED CBO NETWORK API CALLS")
        print("="*65)
        print(f"Captured {len(captured_payloads)} API requests:")
        for idx, call in enumerate(captured_payloads[-5:]):
            print(f"\n--- Request [{idx}] ---")
            print(f"URL: {call['url']}")
            print(f"POST Payload: {call['post_data']}")

        browser.close()
        print("\n🏁 X-Ray run finished! Output in: /workspaces/Dios/spo_test_output.txt")

if __name__ == "__main__":
    run_xray()
