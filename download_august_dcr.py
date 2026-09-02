from playwright.sync_api import sync_playwright
import time, os

CBO_USER = "6958BANWARI"
CBO_PASS = "6958"
LOGIN_URL = "https://dios.myreporting.net/erp/login"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
    context = browser.new_context(viewport={'width': 1440, 'height': 900}, accept_downloads=True)
    page = context.new_page()

    print("[1] Logging in to CBO...")
    page.goto(LOGIN_URL, timeout=60000, wait_until="domcontentloaded")
    page.wait_for_timeout(1500)
    page.fill("input[type='text']:visible", CBO_USER)
    page.fill("input[type='password']:visible", CBO_PASS)
    page.locator("button:visible:has-text('Login'), input[type='submit']:visible, .btn-success:visible").first.click()
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)

    print("[2] Opening 'Date Wise Call Detail'...")
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

    print("[3] Setting BOTH Dates (From: 01/08/2026, To: 31/08/2026)...")
    res = page.evaluate('''() => {
        // Find the 2 distinct datepicker input controls
        // In CBO Syncfusion, they have distinct container blocks or IDs ending with _input
        const allDateInputs = Array.from(document.querySelectorAll('input')).filter(i => 
            (i.placeholder && i.placeholder.includes('DD/MM/YYYY')) || 
            (i.value && (i.value.includes('/') || i.value.includes('-')))
        );

        // Filter to get only UNIQUE controls by taking only elements whose IDs differ
        const uniqueInputs = [];
        const seenIds = new Set();
        for (let inp of allDateInputs) {
            const baseId = inp.id.replace('_input', '').replace('_options', '');
            if (!seenIds.has(baseId)) {
                seenIds.add(baseId);
                uniqueInputs.push(inp);
            }
        }

        if (uniqueInputs.length >= 2) {
            // Set From Date
            uniqueInputs[0].focus();
            uniqueInputs[0].value = '01/08/2026';
            uniqueInputs[0].dispatchEvent(new Event('input', {bubbles: true}));
            uniqueInputs[0].dispatchEvent(new Event('change', {bubbles: true}));
            uniqueInputs[0].blur();

            // Set To Date
            uniqueInputs[1].focus();
            uniqueInputs[1].value = '31/08/2026';
            uniqueInputs[1].dispatchEvent(new Event('input', {bubbles: true}));
            uniqueInputs[1].dispatchEvent(new Event('change', {bubbles: true}));
            uniqueInputs[1].blur();

            return { success: true, from: uniqueInputs[0].value, to: uniqueInputs[1].value };
        }
        return { success: false, found: allDateInputs.length };
    }''')
    print("Date set result:", res)
    time.sleep(1)

    print("[4] Submitting (Clicking GO)...")
    page.evaluate('''() => {
        const btns = Array.from(document.querySelectorAll('button, input[type=button], input[type=submit]'));
        const go = btns.find(b => (b.innerText || b.value || '').trim().toUpperCase().includes('GO'));
        if (go) go.click();
    }''')

    time.sleep(6)

    print("[5] Downloading DCR Excel file...")
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
        print(f"🎉 EXCEL DOWNLOADED: {excel_path}")
    except Exception as e:
        print("Download error:", e)

    page.screenshot(path='/workspaces/Dios/csv_output/dcr_final_august.png')
    print("📸 Screenshot saved: csv_output/dcr_final_august.png")
    browser.close()
