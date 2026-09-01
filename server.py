import os, sys, time, csv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from playwright.sync_api import sync_playwright

app = FastAPI(title="DIOS CBO Primary API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
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

def execute_cbo_fetch(from_month: str, to_month: str, fy_year: str):
    os.makedirs("csv_output", exist_ok=True)
    direct_report_url = f"https://dios.myreporting.net/RPT/PerformanceReview.aspx?format=Primary%20Sales&wise=P&DOC_TYPE=SS&RPT_HEADER=Monthly%20Sales-Summary&CBOYN=Y&FY_YEAR={fy_year}&COMPANY_CODE=DIOS&PA_ID=6958&DESIG_ID=1&DESIG=BE&PA_NAME=BANWARI%20LAL%20MEENA&HEAD_QTR=UDAIPUR&DIVISION_NAME=DIOS%20GROUP&FMCGYN=N&MENU_STYLE=NONE&ACTION_FROM=ANDROID&LOGIN_PA_ID=6958&LOGIN_COMPANY_ID=1"

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-popup-blocking", "--no-sandbox", "--disable-web-security"]
        )
        
        storage = SESSION_FILE if os.path.exists(SESSION_FILE) else None
        if storage:
            context = browser.new_context(storage_state=storage, viewport={"width": 1440, "height": 900}, accept_downloads=True)
        else:
            context = browser.new_context(viewport={"width": 1440, "height": 900}, accept_downloads=True)

        page = context.new_page()
        page.on("dialog", lambda dialog: dialog.accept())

        # 1. Login check
        page.goto(LOGIN_URL, timeout=60000, wait_until="networkidle")
        page.wait_for_timeout(1000)

        if "login" in page.url.lower() or page.locator("input[type='password']").count() > 0:
            page.fill("input[type='text']:visible", CBO_USER)
            page.fill("input[type='password']:visible", CBO_PASS)
            login_btn = page.locator("button:visible:has-text('Login'), input[type='submit']:visible, .btn-success:visible").first
            if login_btn.count() > 0:
                login_btn.click()
            else:
                page.keyboard.press("Enter")

            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(3000)
            context.storage_state(path=SESSION_FILE)

        # 2. Open Form
        page.goto(direct_report_url, timeout=60000, wait_until="domcontentloaded")
        page.wait_for_timeout(3500)

        # 3. Select From & To Month
        target_frame = None
        for f in page.frames:
            try:
                has_selects = f.evaluate("""([fMonth, tMonth]) => {
                    const selects = Array.from(document.querySelectorAll('select'));
                    const mSelects = selects.filter(s => Array.from(s.options).some(o => o.text.includes('202') || o.text.includes('Aug') || o.text.includes('Apr') || o.text.includes('May')));
                    if (mSelects.length >= 2) {
                        for (let opt of mSelects[0].options) {
                            if (opt.text.toLowerCase().includes(fMonth.toLowerCase()) || opt.text.toLowerCase().includes(fMonth.substring(0,3).toLowerCase())) {
                                mSelects[0].value = opt.value;
                                mSelects[0].dispatchEvent(new Event('change', { bubbles: true }));
                                break;
                            }
                        }
                        for (let opt of mSelects[1].options) {
                            if (opt.text.toLowerCase().includes(tMonth.toLowerCase()) || opt.text.toLowerCase().includes(tMonth.substring(0,3).toLowerCase())) {
                                mSelects[1].value = opt.value;
                                mSelects[1].dispatchEvent(new Event('change', { bubbles: true }));
                                break;
                            }
                        }
                        return true;
                    }
                    return false;
                }""", [from_month, to_month])
                if has_selects:
                    target_frame = f
                    break
            except Exception:
                pass

        if not target_frame:
            target_frame = page.main_frame

        # 4. Click Go
        active_page = page
        try:
            with context.expect_page(timeout=5000) as popup_info:
                target_frame.evaluate("""() => {
                    const btns = Array.from(document.querySelectorAll('button, input, a'));
                    const go = btns.find(b => (b.innerText || b.value || '').trim().toLowerCase() === 'go' || b.id.toLowerCase().includes('btngo'));
                    if (go) go.click();
                }""")
            active_page = popup_info.value
        except Exception:
            target_frame.evaluate("""() => {
                const btns = Array.from(document.querySelectorAll('button, input, a'));
                const go = btns.find(b => (b.innerText || b.value || '').trim().toLowerCase() === 'go' || b.id.toLowerCase().includes('btngo'));
                if (go) go.click();
            }""")

        active_page.wait_for_load_state("domcontentloaded")
        active_page.wait_for_timeout(6000)

        # 5. Extract Data Rows
        scraped_products = []
        for f in active_page.frames:
            rows = f.evaluate("""() => {
                const result = [];
                const allRows = Array.from(document.querySelectorAll('tr'));
                for (let r of allRows) {
                    const cells = Array.from(r.querySelectorAll('td, th')).map(c => c.innerText.trim());
                    if (cells.length >= 2) {
                        result.push(cells);
                    }
                }
                return result;
            }""")

            for r in rows:
                if len(r) >= 2:
                    p_name = r[0]
                    if p_name and not p_name.upper().startswith("PRODUCT") and not p_name.upper().startswith("COUNT") and not p_name.upper().startswith("PRIMARY"):
                        qty = 0
                        val = 0
                        try:
                            qty = float(r[1].replace(',', ''))
                        except Exception:
                            pass
                        try:
                            val = float(r[2].replace(',', ''))
                        except Exception:
                            pass
                        scraped_products.append({
                            "name": p_name,
                            "qty": qty,
                            "value": val
                        })

        # Save to CSV for persistent backup
        out_csv = f"csv_output/Primary_{from_month}_to_{to_month}.csv"
        with open(out_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["PRODUCT NAME", "PRIMARY QTY", "PRIMARY VALUE"])
            for p_item in scraped_products:
                writer.writerow([p_item["name"], p_item["qty"], p_item["value"]])

        browser.close()
        return scraped_products

@app.post("/api/fetch-primary")
def fetch_primary(req: FetchRequest):
    try:
        data = execute_cbo_fetch(req.from_month, req.to_month, req.fy_year)
        if not data:
            raise HTTPException(status_code=404, detail="No data found or CBO report not loaded.")
        
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
