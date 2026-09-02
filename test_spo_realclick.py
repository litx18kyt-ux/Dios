from playwright.sync_api import sync_playwright
import time, os

CBO_USER = "6958BANWARI"
CBO_PASS = "6958"
LOGIN_URL = "https://dios.myreporting.net/erp/login"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
    context = browser.new_context(viewport={'width': 1440, 'height': 900}, accept_downloads=True)
    page = context.new_page()
    page.on('dialog', lambda d: d.accept())

    print("[1] Logging in to CBO...")
    page.goto(LOGIN_URL, timeout=60000, wait_until="domcontentloaded")
    page.wait_for_timeout(1500)
    page.fill("input[type='text']:visible", CBO_USER)
    page.fill("input[type='password']:visible", CBO_PASS)
    page.locator("button:visible:has-text('Login'), input[type='submit']:visible, .btn-success:visible").first.click()
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)

    print("[2] Opening Reports -> Sales & Targets...")
    page.locator("a:has-text('Reports'), span:has-text('Reports')").first.click()
    page.wait_for_timeout(800)

    page.locator("text='Sales & Targets'").first.hover()
    page.wait_for_timeout(1000)

    print("[3] Real Mouse Click on 'SPO Stockist Wise' SPAN...")
    # Click the exact text span
    page.locator("span:has-text('SPO Stockist Wise'), a:has-text('SPO Stockist Wise')").first.click()
    page.wait_for_timeout(4000)

    print(f"\n[4] Page state after click:")
    print("URL:", page.url)

    # Check if a datepicker modal opened
    modal_opened = page.evaluate('''() => {
        const pickers = Array.from(document.querySelectorAll('.e-datepicker, input[role=\"combobox\"]'));
        return pickers.length;
    }''')
    print(f"Datepickers found: {modal_opened}")

    if modal_opened >= 2:
        print("Setting Dates (01/08/2026 to 31/08/2026)...")
        page.evaluate('''() => {
            const allElements = Array.from(document.querySelectorAll('*')).filter(e => e.ej2_instances && e.ej2_instances.length > 0);
            const pickers = allElements.filter(e => e.ej2_instances[0].getModuleName && e.ej2_instances[0].getModuleName() === 'datepicker');
            if (pickers.length >= 2) {
                pickers[0].ej2_instances[0].value = new Date(2026, 7, 1);
                if (pickers[0].ej2_instances[0].dataBind) pickers[0].ej2_instances[0].dataBind();
                pickers[1].ej2_instances[0].value = new Date(2026, 7, 31);
                if (pickers[1].ej2_instances[0].dataBind) pickers[1].ej2_instances[0].dataBind();
            }
            const btns = Array.from(document.querySelectorAll('button, input[type=button], input[type=submit]'));
            const go = btns.find(b => (b.innerText || b.value || '').trim().toUpperCase().includes('GO'));
            if (go) go.click();
        }''')
        time.sleep(6)

    # Check and print table rows
    print("\n[5] Reading Table on screen:")
    for f in page.frames:
        rows = f.evaluate('''() => {
            const trs = Array.from(document.querySelectorAll('tr'));
            return trs.map(r => Array.from(r.querySelectorAll('td, th')).map(c => c.innerText.trim())).filter(r => r.length >= 4);
        }''')
        if len(rows) > 0:
            print(f"🎯 Frame '{f.name}' has {len(rows)} rows!")
            for idx, r in enumerate(rows[:10]):
                print(f"  Row {idx}: {r}")

    # Check Excel Download
    excel_path = "/workspaces/Dios/csv_output/SPO_StockistWise_Aug-2026.xls"
    try:
        with page.expect_download(timeout=10000) as dl_info:
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
        print("Excel download note:", e)

    browser.close()
