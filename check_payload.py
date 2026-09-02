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

    # Click Go using Playwright locator
    btn = form_frame.locator("#btnGo1, #btnGo, input[value*='Go']").first
    btn.click()
    page.wait_for_timeout(5000)

    def handle_request(request):
        if 'GETGROUPEDBYDATAGRID' in request.url:
            print("\n🔥 CAPTURED AJAX REQUEST:")
            print("URL:", request.url)
            print("Method:", request.method)
            print("POST Data:", request.post_data)

    def handle_response(response):
        if 'GETGROUPEDBYDATAGRID' in response.url:
            print("\n📦 CAPTURED AJAX RESPONSE:")
            print("Status:", response.status)
            try:
                print("Response JSON/Text Preview:\n", response.text()[:500])
            except Exception:
                pass

    page.on("request", handle_request)
    page.on("response", handle_response)

    # Click UDAIPUR link
    for f in page.frames:
        u_link = f.locator("a:has-text('UDAIPUR')").first
        if u_link.count() > 0:
            print("Clicking UDAIPUR...")
            u_link.click()
            break

    time.sleep(5)
    browser.close()
