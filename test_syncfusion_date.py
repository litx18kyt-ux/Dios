from playwright.sync_api import sync_playwright
import time

CBO_USER = "6958BANWARI"
CBO_PASS = "6958"
LOGIN_URL = "https://dios.myreporting.net/erp/login"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
    context = browser.new_context(viewport={'width': 1440, 'height': 900}, accept_downloads=True)
    page = context.new_page()

    print("[1] Logging into CBO...")
    page.goto(LOGIN_URL, timeout=60000, wait_until="domcontentloaded")
    page.wait_for_timeout(1500)
    page.fill("input[type='text']:visible", CBO_USER)
    page.fill("input[type='password']:visible", CBO_PASS)
    page.locator("button:visible:has-text('Login'), input[type='submit']:visible, .btn-success:visible").first.click()
    page.wait_for_timeout(3500)

    print("[2] Opening Date Wise Call Detail...")
    page.locator("a:has-text('Reports'), span:has-text('Reports')").first.click()
    page.wait_for_timeout(800)

    page.evaluate('''() => {
        const elms = Array.from(document.querySelectorAll('a, span, li, td'));
        const dcr = elms.find(e => (e.innerText || '').trim() === 'DCR Reports');
        if (dcr) { dcr.dispatchEvent(new MouseEvent('mouseover', {bubbles: true})); dcr.click(); }
    }''')
    page.wait_for_timeout(800)

    page.evaluate('''() => {
        const elms = Array.from(document.querySelectorAll('a, span, li, td'));
        const item = elms.find(e => (e.innerText || '').trim() === 'Date Wise Call Detail');
        if (item) item.click();
    }''')
    page.wait_for_timeout(2500)

    print("\n[3] Setting Date via Syncfusion ej2_instances API...")
    date_info = page.evaluate('''() => {
        // Find all elements with Syncfusion instances
        const allElements = Array.from(document.querySelectorAll('*')).filter(e => e.ej2_instances && e.ej2_instances.length > 0);
        
        // Filter datepickers
        const pickers = allElements.filter(e => e.ej2_instances[0].getModuleName && e.ej2_instances[0].getModuleName() === 'datepicker');

        if (pickers.length >= 2) {
            // August 1, 2026 (Month is 7 in JS because 0-indexed)
            const dFrom = new Date(2026, 7, 1);
            const dTo = new Date(2026, 7, 31);

            pickers[0].ej2_instances[0].value = dFrom;
            if (pickers[0].ej2_instances[0].dataBind) pickers[0].ej2_instances[0].dataBind();

            pickers[1].ej2_instances[0].value = dTo;
            if (pickers[1].ej2_instances[0].dataBind) pickers[1].ej2_instances[0].dataBind();

            return {
                success: true,
                count: pickers.length,
                val1: pickers[0].value,
                val2: pickers[1].value,
                formatted1: pickers[0].ej2_instances[0].value,
                formatted2: pickers[1].ej2_instances[0].value
            };
        }
        return { success: false, total_ej2: allElements.length };
    }''')
    print("Syncfusion Result:", date_info)

    print("\n[4] Submitting (Clicking GO)...")
    page.evaluate('''() => {
        const btns = Array.from(document.querySelectorAll('button, input[type=button], input[type=submit]'));
        const go = btns.find(b => (b.innerText || b.value || '').trim().toUpperCase().includes('GO'));
        if (go) go.click();
    }''')

    time.sleep(6)

    # Check Date in Report Header on Screen
    report_header = page.evaluate('''() => {
        const headers = Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, div, span')).filter(e => (e.innerText || '').includes('From Date'));
        return headers.map(h => h.innerText.trim());
    }''')
    print("\n🎯 REPORT HEADER ON SCREEN:")
    for h in report_header[:3]:
        print(" ->", h)

    # Download Excel
    print("\n[5] Downloading Excel file...")
    excel_path = "/workspaces/Dios/csv_output/DCR_DateWise_Aug-2026.xls"
    try:
        with page.expect_download(timeout=15000) as dl_info:
            page.evaluate('''() => {
                const elms = Array.from(document.querySelectorAll('a, button, i, span, img'));
                const btn = elms.find(e => {
                    const cls = (e.className || '').toLowerCase();
                    const title = (e.getAttribute('title') || '').toLowerCase();
                    return cls.includes('excel') || title.includes('excel') || cls.includes('fa-file-excel');
                });
                if (btn) btn.click();
            }''')
        dl = dl_info.value
        dl.save_as(excel_path)
        print(f"🎉 EXCEL DOWNLOADED TO: {excel_path}")
    except Exception as e:
        print("Download error:", e)

    browser.close()
