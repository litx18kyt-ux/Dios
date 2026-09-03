import os
import sys
import time
import json
from playwright.sync_api import sync_playwright

LOG_FILE = "/workspaces/Dios/spo_test_output.txt"
JSON_OUT = "/workspaces/Dios/cbo_api_response.json"
MODAL_DUMP = "/workspaces/Dios/modal_dump.html"

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

print("=== CBO SPO MASTER API SNIFFER & DOM X-RAY LOG ===\n")

CBO_USER = os.getenv("CBO_USER", "6958BANWARI")
CBO_PASS = os.getenv("CBO_PASS", "6958")
LOGIN_URL = "https://dios.myreporting.net/erp/login"

def run():
    print("🚀 [1/5] Launching Playwright Engine with Deep Network Spy...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
        context = browser.new_context(viewport={"width": 1440, "height": 900}, accept_downloads=True)
        page = context.new_page()
        page.set_default_timeout(25000)

        # 📡 Deep Network Interceptor
        captured_requests = []
        captured_responses = []

        def on_request(req):
            if "apirequest" in req.url or "spo" in req.url.lower():
                try:
                    body = req.post_data
                    captured_requests.append({
                        "url": req.url,
                        "method": req.method,
                        "headers": dict(req.headers),
                        "payload": body
                    })
                except Exception:
                    pass
        page.on("request", on_request)

        def on_response(res):
            if "apirequest" in res.url or "spo" in res.url.lower():
                try:
                    data = res.json()
                    captured_responses.append({
                        "url": res.url,
                        "status": res.status,
                        "json": data
                    })
                except Exception:
                    try:
                        captured_responses.append({
                            "url": res.url,
                            "status": res.status,
                            "text": res.text()[:500]
                        })
                    except Exception:
                        pass
        page.on("response", on_response)

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
        page.wait_for_timeout(4000)

        # 3. Click Filter Funnel Icon to open modal
        print("🔍 [4/5] Clicking Filter Funnel Icon (filter.svg)...")
        page.evaluate('''() => {
            const isVis = el => el && (el.offsetWidth > 0 || el.offsetHeight > 0);
            const imgs = Array.from(document.querySelectorAll("img, a, button, i")).filter(isVis);
            const filterBtn = imgs.find(e => (e.src || '').includes('filter') || (e.className || '').includes('filter') || (e.getAttribute('title') || '').toLowerCase().includes('filter'));
            if (filterBtn) filterBtn.click();
        }''')
        page.wait_for_timeout(2000)

        # 4. DUMP MODAL HTML & LIST EVERY SINGLE INPUT
        print("\n" + "="*65)
        print("🔬 DEEP X-RAY: DUMPING ALL INPUTS & MODAL STRUCTURE")
        print("="*65)

        # Dump Modal HTML
        modal_html = page.evaluate('''() => {
            const dialog = document.querySelector(".modal, .popup, [role='dialog'], .e-dialog, .ui-dialog, div[class*='dialog']") || document.body;
            return dialog ? dialog.outerHTML : document.body.innerHTML;
        }''')
        with open(MODAL_DUMP, "w", encoding="utf-8") as f:
            f.write(modal_html)
        print(f"💾 Saved Modal HTML dump to: {MODAL_DUMP} ({len(modal_html)} bytes)")

        # List every single input across all frames
        for f_idx, f in enumerate(page.frames):
            inputs = f.evaluate('''() => {
                return Array.from(document.querySelectorAll("input, select, ejs-datepicker, textarea")).map(i => ({
                    tag: i.tagName,
                    type: i.type || '',
                    id: i.id || '',
                    name: i.name || '',
                    value: i.value || '',
                    placeholder: i.placeholder || '',
                    className: i.className || '',
                    parentTag: i.parentElement ? i.parentElement.tagName : '',
                    parentClass: i.parentElement ? i.parentElement.className : ''
                }));
            }''')
            print(f"\nFrame [{f_idx}] Elements Count: {len(inputs)}")
            for inp in inputs:
                print(f"   <{inp['tag']} type='{inp['type']}'> id='{inp['id']}' name='{inp['name']}' val='{inp['value']}' ph='{inp['placeholder']}' parent=<{inp['parentTag']}.{inp['parentClass'][:30]}>")

        # Click blue 'GO' button to trigger the network API call
        print("\n🔘 [5/5] Clicking GO Button to trigger CBO API...")
        page.evaluate('''() => {
            const isVis = el => el && (el.offsetWidth > 0 || el.offsetHeight > 0);
            const btns = Array.from(document.querySelectorAll("button, input[type='button'], a")).filter(isVis);
            const goBtn = btns.find(b => (b.innerText || b.value || '').trim().toUpperCase().includes('GO'));
            if (goBtn) goBtn.click();
        }''')
        page.wait_for_timeout(5000)

        browser.close()

    # 5. DUMP INTERCEPTED API CALLS
    print("\n" + "="*65)
    print("📡 CAPTURED CBO API REQUESTS & PAYLOADS")
    print("="*65)
    print(f"Total Requests Captured: {len(captured_requests)}")
    for idx, r in enumerate(captured_requests):
        print(f"\n--- Request [{idx}] ---")
        print(f"URL: {r['url']}")
        print(f"Method: {r['method']}")
        print(f"Payload: {r['payload']}")

    print(f"\nTotal Responses Captured: {len(captured_responses)}")
    if captured_responses:
        with open(JSON_OUT, "w", encoding="utf-8") as f:
            json.dump(captured_responses, f, indent=2)
        print(f"💾 Full JSON response saved to: {JSON_OUT}")
        
        for idx, res in enumerate(captured_responses):
            print(f"Response [{idx}] Status: {res.get('status')}")
            if "json" in res:
                print(f"   Keys: {list(res['json'].keys())}")

    print("\n🏁 Done! All results written to: spo_test_output.txt")

if __name__ == "__main__":
    run()
