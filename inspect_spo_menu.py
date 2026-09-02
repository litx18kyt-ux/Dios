from playwright.sync_api import sync_playwright
import time, json

CBO_USER = "6958BANWARI"
CBO_PASS = "6958"
LOGIN_URL = "https://dios.myreporting.net/erp/login"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
    context = browser.new_context(viewport={'width': 1440, 'height': 900})
    page = context.new_page()

    page.goto(LOGIN_URL, timeout=60000, wait_until="domcontentloaded")
    page.wait_for_timeout(1500)
    page.fill("input[type='text']:visible", CBO_USER)
    page.fill("input[type='password']:visible", CBO_PASS)
    page.locator("button:visible:has-text('Login'), input[type='submit']:visible, .btn-success:visible").first.click()
    page.wait_for_timeout(3500)

    # Click Reports
    page.locator("a:has-text('Reports'), span:has-text('Reports')").first.click()
    page.wait_for_timeout(800)

    # Hover Sales & Targets
    page.evaluate('''() => {
        const elms = Array.from(document.querySelectorAll('a, span, li, td'));
        const st = elms.find(e => (e.innerText || '').trim() === 'Sales & Targets');
        if (st) {
            st.dispatchEvent(new MouseEvent('mouseover', {bubbles: true}));
            st.dispatchEvent(new MouseEvent('mouseenter', {bubbles: true}));
            st.click();
        }
    }''')
    page.wait_for_timeout(1000)

    # Inspect the exact element $Reports/CnfSpoStk_Report
    menu_detail = page.evaluate('''() => {
        const item = document.getElementById('$Reports/CnfSpoStk_Report');
        if (!item) {
            // Find by text
            const all = Array.from(document.querySelectorAll('*')).filter(e => (e.innerText || '').trim() === 'SPO Stockist Wise');
            return { found_by_id: false, found_by_text_count: all.length, elements: all.map(e => e.outerHTML) };
        }
        return {
            found_by_id: true,
            outerHTML: item.outerHTML,
            parentHTML: item.parentElement ? item.parentElement.outerHTML : '',
            attributes: Array.from(item.attributes).map(a => ({name: a.name, value: a.value})),
            children: Array.from(item.children).map(c => c.outerHTML)
        };
    }''')

    print("=== MENU ITEM DETAILS ===")
    print(json.dumps(menu_detail, indent=2))

    browser.close()
