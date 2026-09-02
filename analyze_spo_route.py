from playwright.sync_api import sync_playwright
import time, json

CBO_USER = "6958BANWARI"
CBO_PASS = "6958"
LOGIN_URL = "https://dios.myreporting.net/erp/login"
OUT_TXT = "/workspaces/Dios/spo_analysis.txt"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
    context = browser.new_context(viewport={'width': 1440, 'height': 900})
    page = context.new_page()

    print("[1] Logging into CBO...")
    page.goto(LOGIN_URL, timeout=60000, wait_until="domcontentloaded")
    page.wait_for_timeout(1500)
    page.fill("input[type='text']:visible", CBO_USER)
    page.fill("input[type='password']:visible", CBO_PASS)
    page.locator("button:visible:has-text('Login'), input[type='submit']:visible, .btn-success:visible").first.click()
    page.wait_for_timeout(3500)

    print("[2] Inspecting Navbar Menu Handler & Route Mapping...")
    analysis = page.evaluate('''() => {
        const results = {};
        
        // 1. Search in localStorage for menu configuration
        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            const val = localStorage.getItem(key);
            if (val && (val.includes('CnfSpoStk') || val.includes('SPO Stockist'))) {
                results['localStorageKey_' + key] = val.substring(0, 1500);
            }
        }

        // 2. Inspect Syncfusion Menu Event Handlers
        const menuEl = document.querySelector('ejs-menu, .e-menu-wrapper, [role=\"menubar\"]');
        if (menuEl && menuEl.ej2_instances && menuEl.ej2_instances.length > 0) {
            const menuInst = menuEl.ej2_instances[0];
            results['menuEvents'] = Object.keys(menuInst).filter(k => typeof menuInst[k] === 'function');
            results['hasSelect'] = typeof menuInst.select === 'function';
        }

        // 3. Search window object for router / navigation helpers
        results['windowRoutes'] = Object.keys(window).filter(k => k.toLowerCase().includes('route') || k.toLowerCase().includes('nav') || k.toLowerCase().includes('cbo'));

        return results;
    }''')

    # Also search main JS bundle for "reportwithactionbar"
    print("[3] Searching route definition for reportwithactionbar...")
    import requests, re
    r_js = requests.get("https://dios.myreporting.net/erp/main.351cc31a09a59193.js")
    action_matches = [m.start() for m in re.finditer(r'reportwithactionbar', r_js.text, re.IGNORECASE)]
    snippets = []
    for pos in action_matches[:3]:
        snippets.append(r_js.text[max(0, pos-200):min(len(r_js.text), pos+300)])
    analysis['actionbar_snippets'] = snippets

    with open(OUT_TXT, "w", encoding="utf-8") as f:
        json.dump(analysis, f, indent=2)

    print(f"\n✅ Analysis complete! Saved to {OUT_TXT}")
    browser.close()
