from playwright.sync_api import sync_playwright
import time, json

CBO_USER = "6958BANWARI"
CBO_PASS = "6958"
LOGIN_URL = "https://dios.myreporting.net/erp/login"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
    context = browser.new_context(viewport={'width': 1440, 'height': 900})
    page = context.new_page()

    page.on("request", lambda r: print(f"📡 {r.method} -> {r.url}") if 'myreporting' in r.url and not any(x in r.url for x in ['.png', '.jpg', '.css', '.js']) else None)

    print("[1] Logging into CBO...")
    page.goto(LOGIN_URL, timeout=60000, wait_until="domcontentloaded")
    page.wait_for_timeout(1500)
    page.fill("input[type='text']:visible", CBO_USER)
    page.fill("input[type='password']:visible", CBO_PASS)
    page.locator("button:visible:has-text('Login'), input[type='submit']:visible, .btn-success:visible").first.click()
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)

    print("\n[2] Triggering Syncfusion Menu Select Event...")
    result = page.evaluate('''() => {
        // Find Syncfusion Menu component instance
        const menuEl = document.querySelector('ejs-menu, .e-menu-wrapper, [role=\"menubar\"]');
        const inst = (menuEl && menuEl.ej2_instances) ? menuEl.ej2_instances[0] : null;

        // Search in all window/angular objects for navigation
        const targetId = '$Reports/CnfSpoStk_Report';
        
        let details = {
            menuFound: !!inst,
            menuModuleName: inst ? inst.getModuleName() : null
        };

        // If Syncfusion instance exists, trigger select
        if (inst) {
            // Find the item in inst.items
            const findItem = (items) => {
                for (let it of items) {
                    if (it.id === targetId || (it.text && it.text.includes('SPO Stockist Wise'))) return it;
                    if (it.items) {
                        const sub = findItem(it.items);
                        if (sub) return sub;
                    }
                }
                return null;
            };
            const targetItem = findItem(inst.items || []);
            details.targetItem = targetItem;

            if (targetItem) {
                // Trigger select event directly on component
                if (inst.select) {
                    inst.select({ item: targetItem, element: document.getElementById(targetId) });
                    details.calledSelect = true;
                }
            }
        }

        // Also try clicking the actual li and span with complete MouseEvent chain
        const li = document.getElementById(targetId);
        if (li) {
            const span = li.querySelector('span') || li;
            ['mouseenter', 'mouseover', 'mousedown', 'mouseup', 'click'].forEach(evt => {
                span.dispatchEvent(new MouseEvent(evt, { bubbles: true, cancelable: true, view: window }));
            });
            details.dispatchedEvents = true;
        }

        return details;
    }''')
    print("Execution Result:\n", json.dumps(result, indent=2))

    time.sleep(5)
    print("\n[3] Current URL after trigger:", page.url)

    # Check visible tables or breadcrumbs
    info = page.evaluate('''() => {
        const trs = Array.from(document.querySelectorAll('tr')).map(r => Array.from(r.querySelectorAll('td, th')).map(c => c.innerText.trim())).filter(r => r.length > 2);
        const headers = Array.from(document.querySelectorAll('h1, h2, h3, h4, .breadcrumb, a')).filter(e => (e.innerText || '').includes('SPO') || (e.innerText || '').includes('Stockist')).map(e => e.innerText.trim());
        return { tableRows: trs.length, headers: headers };
    }''')
    print("Page Content:", json.dumps(info, indent=2))

    page.screenshot(path='/workspaces/Dios/csv_output/spo_trigger_result.png')
    browser.close()
