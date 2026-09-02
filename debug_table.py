import sys, time, os, json
from playwright.sync_api import sync_playwright

MONTH_TARGET = "Aug-2026"
FY_TARGET = "2026-2027"
CBO_USER = os.getenv("CBO_USER", "6958BANWARI")
CBO_PASS = os.getenv("CBO_PASS", "6958")
LOGIN_URL = "https://dios.myreporting.net/erp/login"
DIRECT_REPORT_URL = f"https://dios.myreporting.net/RPT/PerformanceReview.aspx?format=Primary%20Sales&wise=P&DOC_TYPE=SS&RPT_HEADER=Monthly%20Sales-Summary&CBOYN=Y&FY_YEAR={FY_TARGET}&COMPANY_CODE=DIOS&PA_ID=6958&DESIG_ID=1&DESIG=BE&PA_NAME=BANWARI%20LAL%20MEENA&HEAD_QTR=UDAIPUR&DIVISION_NAME=DIOS%20GROUP&FMCGYN=N&MENU_STYLE=NONE&ACTION_FROM=ANDROID&LOGIN_PA_ID=6958&LOGIN_COMPANY_ID=1"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
    context = browser.new_context(viewport={'width': 1440, 'height': 900}, accept_downloads=True)
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
            if (id.includes('GROUPING') || id.includes('WISE')) selectByText(s, 'Product');
            if (id.includes('FORMAT')) selectByText(s, 'Primary');
        });
    }''', MONTH_TARGET)

    time.sleep(1)

    form_frame.evaluate('''() => {
        const btn = document.getElementById('btnGo1') || document.getElementById('btnGo') || document.querySelector("button:has-text('Go'), input[value*='Go']");
        if (btn) btn.click();
    }''')

    page.wait_for_load_state("domcontentloaded")
    time.sleep(6)

    # Click UDAIPUR link
    for f in page.frames:
        udaipur_link = f.locator("a:has-text('UDAIPUR')").first
        if udaipur_link.count() > 0:
            udaipur_link.click()
            time.sleep(5)
            break

    # Print exact table structure and first 5 rows with all columns
    for f in page.frames:
        rows_data = f.evaluate('''() => {
            const trs = Array.from(document.querySelectorAll('tr'));
            return trs.map(r => Array.from(r.querySelectorAll('td, th')).map(c => c.innerText.trim())).filter(r => r.length > 0);
        }''')
        if len(rows_data) > 5:
            print(f"=== Table in Frame '{f.name}' (Total {len(rows_data)} rows) ===")
            for idx, r in enumerate(rows_data[:10]):
                print(f"Row {idx}: {r}")

    # Check Excel button details
    excel_info = page.evaluate('''() => {
        const elms = Array.from(document.querySelectorAll('a, button, input'));
        return elms.filter(e => (e.innerText || e.value || '').toLowerCase().includes('excel')).map(e => ({
            tag: e.tagName, id: e.id, onclick: e.getAttribute('onclick'), href: e.getAttribute('href'), class: e.className
        }));
    }''')
    print("\n=== Excel Button Details ===")
    print(json.dumps(excel_info, indent=2))

    browser.close()
