import os, sys, time, csv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from playwright.sync_api import sync_playwright

app = FastAPI(title="DIOS Google Cloud Run API")

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
LOGIN_URL = "https://dios.myreporting.net/erp/login"

@app.get("/")
def root():
    return {"status": "online", "engine": "Google Cloud Run Playwright", "version": "v41.0"}

@app.post("/api/fetch-primary")
def fetch_primary(req: FetchRequest):
    direct_report_url = f"https://dios.myreporting.net/RPT/PerformanceReview.aspx?format=Primary%20Sales&wise=P&DOC_TYPE=SS&RPT_HEADER=Monthly%20Sales-Summary&CBOYN=Y&FY_YEAR={req.fy_year}&COMPANY_CODE=DIOS&PA_ID=6958&DESIG_ID=1&DESIG=BE&PA_NAME=BANWARI%20LAL%20MEENA&HEAD_QTR=UDAIPUR&DIVISION_NAME=DIOS%20GROUP&FMCGYN=N&MENU_STYLE=NONE&ACTION_FROM=ANDROID&LOGIN_PA_ID=6958&LOGIN_COMPANY_ID=1"

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-popup-blocking", "--no-sandbox", "--disable-web-security", "--disable-dev-shm-usage"]
        )
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()
        page.on("dialog", lambda dialog: dialog.accept())

        try:
            # 1. Login
            page.goto(LOGIN_URL, timeout=30000, wait_until="domcontentloaded")
            page.wait_for_timeout(1000)
            
            page.fill("input[type='text']:visible", CBO_USER)
            page.fill("input[type='password']:visible", CBO_PASS)
            
            login_btn = page.locator("button:visible:has-text('Login'), input[type='submit']:visible, .btn-success:visible").first
            if login_btn.count() > 0:
                login_btn.click()
            else:
                page.keyboard.press("Enter")

            page.wait_for_load_state("domcontentloaded")
            page.wait_for_timeout(2500)

            # 2. Open Report Form
            page.goto(direct_report_url, timeout=30000, wait_until="domcontentloaded")
            page.wait_for_timeout(3000)

            # 3. Find Frame with Dropdowns
            target_frame = page.main_frame
            for f in page.frames:
                if f.locator("select").count() >= 2:
                    target_frame = f
                    break

            # 4. Set From & To Month
            target_frame.evaluate("""([fMonth, tMonth]) => {
                const selects = Array.from(document.querySelectorAll('select'));
                const mSelects = selects.filter(s => Array.from(s.options).some(o => o.text.includes('202') || o.text.includes('Aug') || o.text.includes('Apr') || o.text.includes('Jul')));
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
                }
            }""", [req.from_month, req.to_month])

            # 5. Click Go
            active_page = page
            try:
                with context.expect_page(timeout=4000) as popup_info:
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
            active_page.wait_for_timeout(5000)

            # 6. Extract Table Rows
            scraped_products = []
            for f in active_page.frames:
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
                        if p_name and not any(k in p_name.upper() for k in ["PRODUCT", "COUNT", "PRIMARY", "TOTAL", "MONTHLY SALES", "CLOSE"]):
                            qty = 0
                            val = 0
                            try:
                                qty = float(r[1].replace(',', ''))
                            except Exception: pass
                            try:
                                val = float(r[2].replace(',', '')) if len(r) > 2 else 0
                            except Exception: pass
                            
                            if len(p_name) > 2:
                                scraped_products.append({"name": p_name, "qty": qty, "value": val})

            browser.close()

            if not scraped_products:
                raise HTTPException(status_code=404, detail="No products found in CBO.")

            total_qty = sum(item["qty"] for item in scraped_products)
            total_val = sum(item["value"] for item in scraped_products)

            return {
                "success": True,
                "from_month": req.from_month,
                "to_month": req.to_month,
                "count": len(scraped_products),
                "total_qty": total_qty,
                "total_value": total_val,
                "items": scraped_products
            }

        except Exception as e:
            browser.close()
            raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
