from playwright.sync_api import sync_playwright

CBO_USER = "6958BANWARI"
CBO_PASS = "6958"
LOGIN_URL = "https://dios.myreporting.net/erp/login"
DIRECT_REPORT_URL = "https://dios.myreporting.net/RPT/PerformanceReview.aspx?format=Primary%20Sales&wise=P&DOC_TYPE=SS&RPT_HEADER=Monthly%20Sales-Summary&CBOYN=Y&FY_YEAR=2026-2027&COMPANY_CODE=DIOS&PA_ID=6958&DESIG_ID=1&DESIG=BE&PA_NAME=BANWARI%20LAL%20MEENA&HEAD_QTR=UDAIPUR&DIVISION_NAME=DIOS%20GROUP&FMCGYN=N&MENU_STYLE=NONE&ACTION_FROM=ANDROID&LOGIN_PA_ID=6958&LOGIN_COMPANY_ID=1"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
    page = browser.new_page()

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

    btn = form_frame.locator("#btnGo1, #btnGo, input[value*='Go']").first
    btn.click()
    page.wait_for_timeout(5000)

    for f in page.frames:
        info = f.evaluate('''() => {
            const elms = Array.from(document.querySelectorAll('a, span, td')).filter(e => (e.innerText || '').includes('UDAIPUR'));
            return elms.map(e => ({
                tag: e.tagName,
                outerHTML: e.outerHTML,
                onclick: e.getAttribute('onclick'),
                href: e.getAttribute('href')
            }));
        }''')
        if info:
            print("UDAIPUR Elements found:")
            for x in info:
                print(x)

    browser.close()
