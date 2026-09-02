from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
    page = browser.new_page()

    page.goto('https://dios.myreporting.net/erp/login', wait_until='networkidle')

    # Look for encrypt or token generation functions in the JS scripts
    enc_info = page.evaluate('''() => {
        const scripts = Array.from(document.querySelectorAll('script')).map(s => s.src);
        let fnText = '';
        if (window.angular) {
            fnText += 'Angular found; ';
        }
        // Let's inspect jQuery or custom ajax functions
        if (window.$ && window.$.ajax) {
            fnText += 'jQuery ajax found; ';
        }
        return {
            scripts: scripts,
            info: fnText
        };
    }''')
    print("Page JS info:", enc_info)
    browser.close()
