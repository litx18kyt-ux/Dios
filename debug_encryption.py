from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
    page = browser.new_page()

    page.goto('https://dios.myreporting.net/erp/login', wait_until='networkidle')

    # Inspect all scripts and global functions
    info = page.evaluate('''() => {
        const funcs = [];
        for (let k in window) {
            if (typeof window[k] === 'function' && !k.startsWith('webkit') && !k.startsWith('on')) {
                funcs.push(k);
            }
        }
        return {
            windowKeys: Object.keys(window).filter(k => k.toLowerCase().includes('crypto') || k.toLowerCase().includes('enc') || k.toLowerCase().includes('token') || k.toLowerCase().includes('login')),
            scripts: Array.from(document.querySelectorAll('script')).map(s => s.src || 'inline')
        };
    }''')

    print("Login Page Info:", json.dumps(info, indent=2))
    browser.close()
