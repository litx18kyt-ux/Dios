import os, sys, time, csv, re
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from playwright.sync_api import sync_playwright

app = FastAPI(title="DIOS CBO Ultra Fast API")

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
    return {"status": "online", "engine": "DIOS Ultra-Fast 16GB Bot", "ready": True}

@app.post("/api/fetch-primary")
def fetch_primary(req: FetchRequest):
    direct_report_url = f"https://dios.myreporting.net/RPT/PerformanceReview.aspx?format=Primary%20Sales&wise=P&DOC_TYPE=SS&RPT_HEADER=Monthly%20Sales-Summary&CBOYN=Y&FY_YEAR={req.fy_year}&COMPANY_CODE=DIOS&PA_ID=6958&DESIG_ID=1&DESIG=BE&PA_NAME=BANWARI%20LAL%20MEENA&HEAD_QTR=UDAIPUR&DIVISION_NAME=DIOS%20GROUP&FMCGYN=N&MENU_STYLE=NONE&ACTION_FROM=ANDROID&LOGIN_PA_ID=6958&LOGIN_COMPANY_ID=1"

    with sync_playwright() as p:
        # Launch High-Speed Chrome
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage", "--disable-gpu"]
        )
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()

        # ⚡ ULTRA SPEED: Block images & media (Page loads 5x faster)
        page.route("**/*", lambda route: route.abort() if route.request.resource_type in ["image", "media", "font"] else route.continue_())
        page.on("dialog", lambda dialog: dialog.accept())

        try:
            # 1. Quick Login
            page.goto(LOGIN_URL, timeout=20000, wait_until="domcontentloaded")
            page.fill("input[type='text']:visible", CBO_USER)
            page.fill("input[type='password']:visible", CBO_PASS)
            
            btn = page.locator("button:visible:has-text('Login'), input[type='submit']:visible, .btn-success:visible").first
            if btn.count() > 0: btn.click()
            else: page.keyboard.press("Enter")
            page.wait_for_timeout(2000)

            # 2. Report Form
            page.goto(direct_report_url, timeout=20000, wait_until="domcontentloaded")
            page.wait_for_timeout(1500)

            target_frame = page.main_frame
            for f in page.frames:
                if f.locator("select").count() >= 2:
                    target_frame = f
                    break

            # 3. Select Month
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
            }""", [req.from_month, req.to_month])

            # 4. Click Go
            target_frame.evaluate("""() => {
                const btns = Array.from(document.querySelectorAll('button, input, a'));
                const go = btns.find(b => (b.innerText || b.value || '').trim().toLowerCase() === 'go' || b.id.toLowerCase().includes('btngo'));
                if (go) go.click();
            }""")

            page.wait_for_timeout(4000)

            # 5. Fast Data Scrape
            scraped = []
            for f in page.frames:
                rows = f.evaluate("""() => {
                    const res = [];
                    for (let t of document.querySelectorAll('table')) {
                        for (let r of t.querySelectorAll('tr')) {
                            const cells = Array.from(r.querySelectorAll('td, th')).map(c => c.innerText.trim());
                            if (cells.length >= 2) res.push(cells);
                        }
                    }
                    return res;
                }""")
                for r in rows:
                    if len(r) >= 2:
                        p_name = r[0]
                        if p_name and not any(k in p_name.upper() for k in ["PRODUCT", "COUNT", "PRIMARY", "TOTAL"]):
                            try:
                                qty = float(r[1].replace(',', ''))
                                val = float(r[2].replace(',', '')) if len(r) > 2 else 0
                                scraped.append({"name": p_name, "qty": qty, "value": val})
                            except Exception: pass

            browser.close()

            if not scraped:
                raise HTTPException(status_code=404, detail="No data returned from CBO.")

            total_qty = sum(item["qty"] for item in scraped)
            total_val = sum(item["value"] for item in scraped)

            return {
                "success": True,
                "from_month": req.from_month,
                "to_month": req.to_month,
                "count": len(scraped),
                "total_qty": total_qty,
                "total_value": total_val,
                "items": scraped
            }
        except Exception as e:
            browser.close()
            raise HTTPException(status_code=500, detail=str(e))
