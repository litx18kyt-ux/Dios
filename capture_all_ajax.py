from playwright.sync_api import sync_playwright
import time, json

CBO_USER = "6958BANWARI"
CBO_PASS = "6958"
LOGIN_URL = "https://dios.myreporting.net/erp/login"
DIRECT_REPORT_URL = "https://dios.myreporting.net/RPT/PerformanceReview.aspx?format=Primary%20Sales&wise=P&DOC_TYPE=SS&RPT_HEADER=Monthly%20Sales-Summary&CBOYN=Y&FY_YEAR=2026-2027&COMPANY_CODE=DIOS&PA_ID=6958&DESIG_ID=1&DESIG=BE&PA_NAME=BANWARI%20LAL%20MEENA&HEAD_QTR=UDAIPUR&DIVISION_NAME=DIOS%20GROUP&FMCGYN=N&MENU_STYLE=NONE&ACTION_FROM=ANDROID&LOGIN_PA_ID=6958&LOGIN_COMPANY_ID=1"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
    context = browser.new_context(viewport={'width': 1440, 'height': 900})
    page = context.new_page()

    page.goto(LOGIN_URL, timeout=60000, wait_until="domcontentloaded")
    page.wait_for_timeout(1500)
    page.fill("input[type='text']", CBO_USER)
    page.fill("input[type='password']", CBO_PASS)
    page.keyboard.press("Enter")
    page.wait_for_timeout(3500)

    page.goto(DIRECT_REPORT_URL, timeout=60000, wait_until="domcontentloaded")
    page.wait_for_timeout(4000)

    form_frame = page.main_frame
    for f in page.frames:
        if f.locator('select#MFDATE').count() > 0:
            form_frame = f
            break

    # Select month Aug-2026 in dropdowns
    form_frame.evaluate('''(target) => {
        const selectByText = (sel, textMatch) => {
            if (!sel) return;
            for (let o of sel.options) {
                if (o.text.toLowerCase().includes(textMatch.toLowerCase()) || o.text.toLowerCase().includes(target.substring(0,3).toLowerCase())) {
                    sel.value = o.value;
                    sel.dispatchEvent(new Event('change', {bubbles: true}));
                    break;
                }
            }
        };
        const selects = Array.from(document.querySelectorAll('select'));
        selects.forEach(s => {
            const id = (s.id || s.name || '').toUpperCase();
            if (id.includes('FDATE')) selectByText(s, target);
            if (id.includes('TDATE')) selectByText(s, target);
        });
    }''', 'Aug-2026')

    btn = form_frame.locator("#btnGo1, #btnGo, input[value*='Go']").first
    btn.click()
    page.wait_for_timeout(5000)

    # Listen to all AJAX requests after clicking UDAIPUR
    def on_request(req):
        if req.method == "POST" and "PerformanceReview.aspx" in req.url:
            print(f"\n📡 Request URL: {req.url}")
            print(f"👉 Payload: {req.post_data}")

    def on_response(resp):
        if "PerformanceReview.aspx" in resp.url and resp.request.method == "POST":
            try:
                data = resp.text()
                if "CALGYM" in data or "Table" in data:
                    print(f"📦 Response ({len(data)} bytes): {data[:300]}")
                    with open(f"/workspaces/Dios/product_response.json", "w", encoding="utf-8") as f:
                        f.write(data)
            except Exception:
                pass

    page.on("request", on_request)
    page.on("response", on_response)

    print("\n[5] Clicking UDAIPUR...")
    for f in page.frames:
        u_link = f.locator("a:has-text('UDAIPUR')").first
        if u_link.count() > 0:
            u_link.click()
            break

    time.sleep(6)
    browser.close()
