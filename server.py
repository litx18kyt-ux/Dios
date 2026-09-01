import os, sys, time, csv, re
import urllib.request
import urllib.parse
import http.cookiejar
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="DIOS CBO Primary API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class FetchRequest(BaseModel):
    from_month: str = "Aug-2026"
    to_month: str = "Aug-2026"
    fy_year: str = "2026-2027"

CBO_USER = os.getenv("CBO_USER", "6958BANWARI")
CBO_PASS = os.getenv("CBO_PASS", "6958")
SESSION_FILE = "cbo_session.json"
LOGIN_URL = "https://dios.myreporting.net/erp/login"

@app.get("/")
def root():
    return {"status": "online", "service": "DIOS CBO Playwright Bot", "version": "32.0"}

# FAST ENGINE 1: High-Speed Direct HTTP Session
def fast_http_scrape(from_month: str, to_month: str, fy_year: str):
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    # Step 1: Login
    login_data = urllib.parse.urlencode({
        "username": CBO_USER,
        "password": CBO_PASS,
        "txtUserName": CBO_USER,
        "txtPassword": CBO_PASS
    }).encode('utf-8')

    req1 = urllib.request.Request(LOGIN_URL, data=login_data, headers=headers)
    try:
        opener.open(req1, timeout=15)
    except Exception:
        pass

    # Step 2: Open Report Form
    report_url = f"https://dios.myreporting.net/RPT/PerformanceReview.aspx?format=Primary%20Sales&wise=P&DOC_TYPE=SS&RPT_HEADER=Monthly%20Sales-Summary&CBOYN=Y&FY_YEAR={fy_year}&COMPANY_CODE=DIOS&PA_ID=6958&DESIG_ID=1&DESIG=BE&PA_NAME=BANWARI%20LAL%20MEENA&HEAD_QTR=UDAIPUR&DIVISION_NAME=DIOS%20GROUP&FMCGYN=N&MENU_STYLE=NONE&ACTION_FROM=ANDROID&LOGIN_PA_ID=6958&LOGIN_COMPANY_ID=1"
    
    req2 = urllib.request.Request(report_url, headers=headers)
    resp2 = opener.open(req2, timeout=20)
    html1 = resp2.read().decode('utf-8', errors='ignore')

    # Extract ASP.NET Hidden Fields
    def get_val(name, text):
        m = re.search(r'name="' + name + r'"[^>]*value="([^"]*)"', text, re.IGNORECASE)
        return m.group(1) if m else ""

    viewstate = get_val('__VIEWSTATE', html1)
    viewstategen = get_val('__VIEWSTATEGENERATOR', html1)
    eventval = get_val('__EVENTVALIDATION', html1)

    # Helper to find Month Option Value
    def find_opt(select_id, month_str, text):
        sel_match = re.search(r'<select[^>]*id="' + select_id + r'"[\s\S]*?</select>', text, re.IGNORECASE)
        if not sel_match:
            return month_str
        opts = re.findall(r'<option[^>]*value="([^"]*)"[^>]*>([\s\S]*?)</option>', sel_match.group(0), re.IGNORECASE)
        for val, opt_text in opts:
            if month_str.lower() in opt_text.lower() or month_str[:3].lower() in opt_text.lower():
                return val
        return month_str

    f_val = find_opt('MFDATE', from_month, html1)
    t_val = find_opt('MTDATE', to_month, html1)

    # Step 3: Postback to get table
    post_params = {
        "__VIEWSTATE": viewstate,
        "__VIEWSTATEGENERATOR": viewstategen,
        "__EVENTVALIDATION": eventval,
        "MFDATE": f_val,
        "MTDATE": t_val,
        "btnGo": "Go",
        "MGROUPING_ID": "0",
        "MDDLSUMMARY": "0",
        "MSTAFF_TYPE": "1",
        "MPA_ID": "6958"
    }
    post_data = urllib.parse.urlencode(post_params).encode('utf-8')
    req3 = urllib.request.Request(report_url, data=post_data, headers={**headers, "Content-Type": "application/x-www-form-urlencoded", "Referer": report_url})
    resp3 = opener.open(req3, timeout=25)
    html2 = resp3.read().decode('utf-8', errors='ignore')

    # Parse rows
    scraped = []
    rows = re.findall(r'<tr[^>]*>([\s\S]*?)</tr>', html2, re.IGNORECASE)
    for r in rows:
        cells = re.findall(r'<t[dh][^>]*>([\s\S]*?)</t[dh]>', r, re.IGNORECASE)
        if len(cells) >= 2:
            clean = [re.sub(r'<[^>]+>', '', c).replace('&nbsp;', ' ').strip() for c in cells]
            p_name = clean[0]
            if p_name and not any(k in p_name.upper() for k in ["PRODUCT", "COUNT", "PRIMARY", "TOTAL"]):
                qty_s = clean[1].replace(',', '') if len(clean) > 1 else '0'
                val_s = clean[2].replace(',', '') if len(clean) > 2 else '0'
                try:
                    qty = float(qty_s)
                    val = float(val_s)
                    scraped.append({"name": p_name, "qty": qty, "value": val})
                except Exception:
                    pass

    return scraped

# ENGINE 2: Playwright Headless Browser Fallback
def playwright_scrape(from_month: str, to_month: str, fy_year: str):
    from playwright.sync_api import sync_playwright
    direct_report_url = f"https://dios.myreporting.net/RPT/PerformanceReview.aspx?format=Primary%20Sales&wise=P&DOC_TYPE=SS&RPT_HEADER=Monthly%20Sales-Summary&CBOYN=Y&FY_YEAR={fy_year}&COMPANY_CODE=DIOS&PA_ID=6958&DESIG_ID=1&DESIG=BE&PA_NAME=BANWARI%20LAL%20MEENA&HEAD_QTR=UDAIPUR&DIVISION_NAME=DIOS%20GROUP&FMCGYN=N&MENU_STYLE=NONE&ACTION_FROM=ANDROID&LOGIN_PA_ID=6958&LOGIN_COMPANY_ID=1"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--disable-popup-blocking", "--no-sandbox", "--disable-web-security"])
        storage = SESSION_FILE if os.path.exists(SESSION_FILE) else None
        context = browser.new_context(storage_state=storage, viewport={"width": 1440, "height": 900}) if storage else browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()
        page.on("dialog", lambda dialog: dialog.accept())

        # Login
        page.goto(LOGIN_URL, timeout=60000, wait_until="networkidle")
        if "login" in page.url.lower() or page.locator("input[type='password']").count() > 0:
            page.fill("input[type='text']:visible", CBO_USER)
            page.fill("input[type='password']:visible", CBO_PASS)
            btn = page.locator("button:visible:has-text('Login'), input[type='submit']:visible, .btn-success:visible").first
            if btn.count() > 0: btn.click()
            else: page.keyboard.press("Enter")
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(3000)
            context.storage_state(path=SESSION_FILE)

        # Form
        page.goto(direct_report_url, timeout=60000, wait_until="domcontentloaded")
        page.wait_for_timeout(3500)

        target_frame = page.main_frame
        for f in page.frames:
            if f.locator("select").count() >= 2:
                target_frame = f
                break

        target_frame.evaluate("""([fMonth, tMonth]) => {
            const selects = Array.from(document.querySelectorAll('select'));
            const mSelects = selects.filter(s => Array.from(s.options).some(o => o.text.includes('202') || o.text.includes('Aug') || o.text.includes('Apr')));
            if (mSelects.length >= 2) {
                for (let opt of mSelects[0].options) {
                    if (opt.text.toLowerCase().includes(fMonth.toLowerCase()) || opt.text.toLowerCase().includes(fMonth.substring(0,3).toLowerCase())) {
                        mSelects[0].value = opt.value; mSelects[0].dispatchEvent(new Event('change', { bubbles: true })); break;
                    }
                }
                for (let opt of mSelects[1].options) {
                    if (opt.text.toLowerCase().includes(tMonth.toLowerCase()) || opt.text.toLowerCase().includes(tMonth.substring(0,3).toLowerCase())) {
                        mSelects[1].value = opt.value; mSelects[1].dispatchEvent(new Event('change', { bubbles: true })); break;
                    }
                }
            }
        }""", [from_month, to_month])

        # Click Go
        target_frame.evaluate("""() => {
            const btns = Array.from(document.querySelectorAll('button, input, a'));
            const go = btns.find(b => (b.innerText || b.value || '').trim().toLowerCase() === 'go' || b.id.toLowerCase().includes('btngo'));
            if (go) go.click();
        }""")

        page.wait_for_timeout(6000)

        scraped = []
        for f in page.frames:
            rows = f.evaluate("""() => {
                const result = [];
                const allRows = Array.from(document.querySelectorAll('tr'));
                for (let r of allRows) {
                    const cells = Array.from(r.querySelectorAll('td, th')).map(c => c.innerText.trim());
                    if (cells.length >= 2) result.push(cells);
                }
                return result;
            }""")
            for r in rows:
                if len(r) >= 2:
                    p_name = r[0]
                    if p_name and not any(k in p_name.upper() for k in ["PRODUCT", "COUNT", "PRIMARY"]):
                        try:
                            qty = float(r[1].replace(',', ''))
                            val = float(r[2].replace(',', '')) if len(r) > 2 else 0
                            scraped.append({"name": p_name, "qty": qty, "value": val})
                        except Exception: pass
        browser.close()
        return scraped

@app.post("/api/fetch-primary")
def fetch_primary(req: FetchRequest):
    data = []
    # 1. Try Fast HTTP Scrape (1.5 seconds)
    try:
        data = fast_http_scrape(req.from_month, req.to_month, req.fy_year)
    except Exception as e:
        print(f"Fast HTTP failed: {e}, switching to Playwright...")

    # 2. If needed, fallback to Playwright
    if not data or len(data) == 0:
        try:
            data = playwright_scrape(req.from_month, req.to_month, req.fy_year)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    if not data:
        raise HTTPException(status_code=404, detail="No data returned from CBO.")

    total_qty = sum(item["qty"] for item in data)
    total_val = sum(item["value"] for item in data)

    return {
        "success": True,
        "from_month": req.from_month,
        "to_month": req.to_month,
        "count": len(data),
        "total_qty": total_qty,
        "total_value": total_val,
        "items": data
    }
