import os
import sys
import time
import re
from playwright.sync_api import sync_playwright

LOG_FILE = "/workspaces/Dios/spo_test_output.txt"
DUMP_FILE = "/workspaces/Dios/full_cbo_page.html"

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

print("=== CBO ACTUAL SOURCE CODE DUMP & X-RAY ===\n")

CBO_USER = os.getenv("CBO_USER", "6958BANWARI")
CBO_PASS = os.getenv("CBO_PASS", "6958")
LOGIN_URL = "https://dios.myreporting.net/erp/login"

def run():
    print("🚀 [1/3] Launching Browser...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
        context = browser.new_context(viewport={"width": 1440, "height": 900}, accept_downloads=True)
        page = context.new_page()
        page.set_default_timeout(30000)

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

        # 2. Open Reports -> Sales & Targets -> SPO Stockist Wise
        print("🧭 Navigating to SPO Stockist Wise...")
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
        page.wait_for_timeout(4000)

        # 3. Click Filter Funnel icon
        print("🔍 Clicking Filter Funnel...")
        page.evaluate('''() => {
            const imgs = Array.from(document.querySelectorAll("img, a, button, i"));
            const filterBtn = imgs.find(e => (e.src || '').includes('filter') || (e.className || '').includes('filter') || (e.getAttribute('title') || '').toLowerCase().includes('filter'));
            if (filterBtn) filterBtn.click();
        }''')
        page.wait_for_timeout(2000)

        # 4. Dump entire page HTML
        print(f"💾 [2/3] Dumping full DOM to: {DUMP_FILE}...")
        full_html = page.content()
        with open(DUMP_FILE, "w", encoding="utf-8") as f:
            f.write(full_html)
        print(f"   Dumped {len(full_html)} characters of HTML!")

        browser.close()

    # 5. Extract the exact code around From Date, To Date, and GO button
    print("\n" + "="*65)
    print("🔬 [3/3] EXTRACTING CBO'S EXACT CODE FOR DATE & BUTTONS")
    print("="*65)

    if os.path.exists(DUMP_FILE):
        with open(DUMP_FILE, "r", encoding="utf-8") as f:
            html = f.read()

        # Search 1: Where is 'From Date'?
        from_matches = [m.start() for m in re.finditer(r'From\s*Date', html, re.IGNORECASE)]
        print(f"\nFound {len(from_matches)} matches for 'From Date':")
        for idx, pos in enumerate(from_matches[:3]):
            snippet = html[max(0, pos - 150) : min(len(html), pos + 400)]
            print(f"\n--- Snippet [{idx}] around 'From Date' ---")
            print(snippet.strip())

        # Search 2: Where is 'To Date'?
        to_matches = [m.start() for m in re.finditer(r'To\s*Date', html, re.IGNORECASE)]
        print(f"\nFound {len(to_matches)} matches for 'To Date':")
        for idx, pos in enumerate(to_matches[:2]):
            snippet = html[max(0, pos - 150) : min(len(html), pos + 400)]
            print(f"\n--- Snippet [{idx}] around 'To Date' ---")
            print(snippet.strip())

        # Search 3: Where is 'GO' or buttons?
        go_matches = [m.start() for m in re.finditer(r'>\s*GO\s*<', html, re.IGNORECASE)]
        print(f"\nFound {len(go_matches)} matches for button '> GO <':")
        for idx, pos in enumerate(go_matches[:2]):
            snippet = html[max(0, pos - 200) : min(len(html), pos + 250)]
            print(f"\n--- Snippet [{idx}] around 'GO' button ---")
            print(snippet.strip())

        # Search 4: List all inputs and their IDs/Classes
        all_inputs = re.findall(r'<input[^>]*>', html, re.IGNORECASE)
        print(f"\nTotal <input> tags found in entire HTML: {len(all_inputs)}")
        for i_idx, inp in enumerate(all_inputs):
            print(f"   Input [{i_idx}]: {inp}")

    print("\n🏁 Analysis Complete! All snippets printed in: spo_test_output.txt")

if __name__ == "__main__":
    run()
