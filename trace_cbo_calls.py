from playwright.sync_api import sync_playwright
import time, json

CBO_USER = "6958BANWARI"
CBO_PASS = "6958"
LOGIN_URL = "https://dios.myreporting.net/erp/login"
DIRECT_REPORT_URL = "https://dios.myreporting.net/RPT/PerformanceReview.aspx?format=Primary%20Sales&wise=P&DOC_TYPE=SS&RPT_HEADER=Monthly%20Sales-Summary&CBOYN=Y&FY_YEAR=2026-2027&COMPANY_CODE=DIOS&PA_ID=6958&DESIG_ID=1&DESIG=BE&PA_NAME=BANWARI%20LAL%20MEENA&HEAD_QTR=UDAIPUR&DIVISION_NAME=DIOS%20GROUP&FMCGYN=N&MENU_STYLE=NONE&ACTION_FROM=ANDROID&LOGIN_PA_ID=6958&LOGIN_COMPANY_ID=1"

network_log = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
    context = browser.new_context(viewport={'width': 1440, 'height': 900})
    page = context.new_page()

    def log_request(req):
        if 'myreporting.net' in req.url and req.resource_type in ['xhr', 'fetch', 'document']:
            network_log.append({
                'url': req.url,
                'method': req.method,
                'headers': req.headers,
                'post_data': req.post_data
            })

    page.on("request", log_request)

    print("[1] Logging in...")
    page.goto(LOGIN_URL, timeout=60000, wait_until="domcontentloaded")
    page.wait_for_timeout(1500)
    page.fill("input[type='text']", CBO_USER)
    page.fill("input[type='password']", CBO_PASS)
    page.keyboard.press("Enter")
    page.wait_for_timeout(3500)

    print("[2] Opening Report...")
    page.goto(DIRECT_REPORT_URL, timeout=60000, wait_until="domcontentloaded")
    page.wait_for_timeout(4000)

    form_frame = page.main_frame
    for f in page.frames:
        if f.locator('select#MFDATE').count() > 0:
            form_frame = f
            break

    print("[3] Clicking Go...")
    btn = form_frame.locator("#btnGo1, #btnGo, input[value*='Go']").first
    btn.click()
    page.wait_for_timeout(5000)

    print("[4] Clicking UDAIPUR...")
    for f in page.frames:
        u_link = f.locator("a:has-text('UDAIPUR')").first
        if u_link.count() > 0:
            u_link.click()
            break

    page.wait_for_timeout(5000)

    with open('/workspaces/Dios/network_trace.json', 'w', encoding='utf-8') as f:
        json.dump(network_log, f, indent=2)

    print("✅ Network trace saved! Total requests:", len(network_log))
    browser.close()
