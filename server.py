import os, sys, time, io
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel
from playwright.sync_api import sync_playwright

app = FastAPI(title="DIOS CBO API")

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

def navigate_to_report(page, req: FetchRequest):
    direct_report_url = f"https://dios.myreporting.net/RPT/PerformanceReview.aspx?format=Primary%20Sales&wise=P&DOC_TYPE=SS&RPT_HEADER=Monthly%20Sales-Summary&CBOYN=Y&FY_YEAR={req.fy_year}&COMPANY_CODE=DIOS&PA_ID=6958&DESIG_ID=1&DESIG=BE&PA_NAME=BANWARI%20LAL%20MEENA&HEAD_QTR=UDAIPUR&DIVISION_NAME=DIOS%20GROUP&FMCGYN=N&MENU_STYLE=NONE&ACTION_FROM=ANDROID&LOGIN_PA_ID=6958&LOGIN_COMPANY_ID=1"

    # Login
    page.goto(LOGIN_URL, timeout=60000, wait_until="domcontentloaded")
    page.wait_for_timeout(1500)
    page.fill("input[type='text']:visible", CBO_USER)
    page.fill("input[type='password']:visible", CBO_PASS)
    page.keyboard.press("Enter")
    page.wait_for_timeout(3500)

    # Open Report Form
    page.goto(direct_report_url, timeout=60000, wait_until="domcontentloaded")
    page.wait_for_timeout(4000)

    form_frame = page.main_frame
    for f in page.frames:
        if f.locator("select#MFDATE").count() > 0 or f.locator('select[name*="FDATE"]').count() > 0:
            form_frame = f
            break

    # Select Month
    form_frame.evaluate('''(target) => {
        const selectByText = (sel, textMatch) => {
            if (!sel) return;
            for (let o of sel.options) {
                if (o.text.toLowerCase().includes(textMatch.toLowerCase()) || o.text.toLowerCase().includes(target.substring(0,3).toLowerCase())) {
                    sel.value = o.value;
                    sel.dispatchEvent(new Event('change', {bubbles: true}));
                    break;
                }
            }
        };
        const selects = Array.from(document.querySelectorAll('select'));
        selects.forEach(s => {
            const id = (s.id || s.name || '').toUpperCase();
            if (id.includes('FDATE')) selectByText(s, target);
            if (id.includes('TDATE')) selectByText(s, target);
            if (id.includes('GROUPING') || id.includes('WISE')) selectByText(s, 'Product');
            if (id.includes('FORMAT')) selectByText(s, 'Primary');
        });
    }''', req.from_month)

    time.sleep(1)

    # Click Go
    active_page = page
    try:
        with page.context.expect_page(timeout=5000) as popup_info:
            form_frame.evaluate('''() => {
                const btn = document.getElementById('btnGo1') || document.getElementById('btnGo') || document.querySelector("button:has-text('Go'), input[value*='Go']");
                if (btn) btn.click();
            }''')
        active_page = popup_info.value
    except Exception:
        form_frame.evaluate('''() => {
            const btn = document.getElementById('btnGo1') || document.getElementById('btnGo') || document.querySelector("button:has-text('Go'), input[value*='Go']");
            if (btn) btn.click();
        }''')

    active_page.wait_for_load_state("domcontentloaded")
    time.sleep(6)

    # Click UDAIPUR to drill down
    for f in active_page.frames:
        clicked = f.evaluate('''() => {
            const links = Array.from(document.querySelectorAll('a, span, td'));
            const uLink = links.find(el => el.innerText && el.innerText.trim().toUpperCase() === 'UDAIPUR');
            if (uLink) { uLink.click(); return true; }
            return false;
        }''')
        if clicked:
            time.sleep(5)
            break

    return active_page

@app.get("/")
def root():
    return {"status": "online", "engine": "Playwright Dual Engine", "version": "v50.0"}

@app.post("/api/fetch-primary")
def fetch_primary(req: FetchRequest):
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-popup-blocking", "--no-sandbox", "--disable-web-security", "--disable-dev-shm-usage"]
        )
        context = browser.new_context(viewport={"width": 1440, "height": 900}, accept_downloads=True)
        page = context.new_page()
        page.on("dialog", lambda dialog: dialog.accept())

        try:
            active_page = navigate_to_report(page, req)

            # Extract Table Rows
            scraped_products = []
            for f in active_page.frames:
                table_data = f.evaluate('''() => {
                    const result = [];
                    const trs = Array.from(document.querySelectorAll('tr'));
                    for (let tr of trs) {
                        const cells = Array.from(tr.querySelectorAll('td, th')).map(c => c.innerText.trim());
                        if (cells.length >= 2) result.push(cells);
                    }
                    return result;
                }''')

                for r in table_data:
                    first_cell = r[0]
                    if not first_cell or any(k in first_cell.upper() for k in ['PRODUCT', 'COUNT', 'PRIMARY SALES', 'TOTAL', 'MONTHLY SALES', 'HEAD QTR', 'OPTIONS', 'COLUMNS', 'EXCEL', 'PDF', 'S.N']):
                        continue
                    
                    nums = []
                    for c in r[1:]:
                        clean_c = c.replace(',', '').replace('₹', '').strip()
                        try:
                            nums.append(float(clean_c))
                        except ValueError:
                            pass

                    if len(nums) >= 2:
                        scraped_products.append({'name': first_cell, 'qty': nums[0], 'value': nums[1]})
                    elif len(nums) == 1:
                        scraped_products.append({'name': first_cell, 'qty': nums[0], 'value': 0})

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

@app.post("/api/download-primary-excel")
def download_excel_endpoint(req: FetchRequest):
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-popup-blocking", "--no-sandbox", "--disable-web-security", "--disable-dev-shm-usage"]
        )
        context = browser.new_context(viewport={"width": 1440, "height": 900}, accept_downloads=True)
        page = context.new_page()
        page.on("dialog", lambda dialog: dialog.accept())

        try:
            active_page = navigate_to_report(page, req)

            # Trigger Excel download from top right button
            download_file_path = f"/tmp/Primary_{req.from_month}.xls"
            downloaded = False
            for f in active_page.frames:
                try:
                    excel_btn = f.locator("a:has-text('Excel'), button:has-text('Excel'), [id*='Excel'], [id*='excel'], img[title*='Excel']").first
                    if excel_btn.count() > 0:
                        with active_page.expect_download(timeout=15000) as dl_info:
                            f.evaluate('''() => {
                                const btn = Array.from(document.querySelectorAll('a, button, input, img')).find(e => 
                                    (e.innerText || e.value || e.title || e.id || '').toLowerCase().includes('excel')
                                );
                                if (btn) btn.click();
                            }''')
                        dl = dl_info.value
                        dl.save_as(download_file_path)
                        downloaded = True
                        break
                except Exception:
                    pass

            browser.close()

            if not downloaded or not os.path.exists(download_file_path):
                raise HTTPException(status_code=500, detail="Could not download Excel from CBO.")

            with open(download_file_path, "rb") as f:
                content = f.read()

            return Response(
                content=content,
                media_type="application/vnd.ms-excel",
                headers={"Content-Disposition": f"attachment; filename=CBO_Primary_{req.from_month}.xls"}
            )
        except Exception as e:
            browser.close()
            raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
