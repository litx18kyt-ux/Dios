from playwright.sync_api import sync_playwright
import time

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

    # Click Go
    form_frame.evaluate('''() => {
        const btn = document.getElementById('btnGo1') || document.getElementById('btnGo') || document.querySelector("button:has-text('Go'), input[value*='Go']");
        if (btn) btn.click();
    }''')
    page.wait_for_timeout(5000)

    # Find UDAIPUR link details
    for f in page.frames:
        u_info = f.evaluate('''() => {
            const links = Array.from(document.querySelectorAll('a'));
            return links.filter(a => (a.innerText || '').includes('UDAIPUR')).map(a => ({
                text: a.innerText,
                href: a.getAttribute('href'),
                onclick: a.getAttribute('onclick')
            }));
        }''')
        if u_info:
            print("🎯 UDAIPUR LINK INFO:", u_info)

    # Now let's capture the request when clicking UDAIPUR
    page.on("request", lambda req: print(f"👉 Request on Click: {req.method} -> {req.url}"))
    
    for f in page.frames:
        f.evaluate('''() => {
            const links = Array.from(document.querySelectorAll('a, span, td'));
            const uLink = links.find(el => el.innerText && el.innerText.trim().toUpperCase() === 'UDAIPUR');
            if (uLink) uLink.click();
        }''')

    time.sleep(5)
    browser.close()
