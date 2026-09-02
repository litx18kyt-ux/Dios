from playwright.sync_api import sync_playwright
import json

CBO_USER = "6958BANWARI"
CBO_PASS = "6958"
LOGIN_URL = "https://dios.myreporting.net/erp/login"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
    context = browser.new_context(viewport={'width': 1440, 'height': 900})
    page = context.new_page()

    auth_data = {}

    def on_response(res):
        if '/api/token' in res.url:
            print("🔑 /api/token Response:")
            try:
                auth_data['token'] = res.json()
                print(json.dumps(res.json(), indent=2))
            except Exception:
                pass

    page.on("response", on_response)

    page.goto(LOGIN_URL, wait_until='networkidle')
    page.fill("input[type='text']", CBO_USER)
    page.fill("input[type='password']", CBO_PASS)
    page.keyboard.press("Enter")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)

    # Dump LocalStorage, SessionStorage & Cookies
    storage = page.evaluate('''() => {
        return {
            localStorage: Object.keys(localStorage).map(k => ({key: k, val: localStorage.getItem(k)})),
            sessionStorage: Object.keys(sessionStorage).map(k => ({key: k, val: sessionStorage.getItem(k)}))
        };
    }''')
    cookies = context.cookies()

    print("\n--- COOKIES ---")
    for c in cookies:
        print(f"{c['name']} = {c['value']}")

    print("\n--- LOCAL STORAGE KEYS ---")
    for item in storage['localStorage']:
        if any(k in item['key'].lower() for k in ['token', 'user', 'auth', 'pass', 'pa_id', 'login']):
            print(f"{item['key']} = {item['val'][:150]}")

    with open('/workspaces/Dios/auth_dump.json', 'w', encoding='utf-8') as f:
        json.dump({'auth_data': auth_data, 'storage': storage, 'cookies': cookies}, f, indent=2)

    browser.close()
