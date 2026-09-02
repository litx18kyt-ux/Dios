from playwright.sync_api import sync_playwright
import time, json

CBO_USER = "6958BANWARI"
CBO_PASS = "6958"
LOGIN_URL = "https://dios.myreporting.net/erp/login"
DIRECT_REPORT_URL = "https://dios.myreporting.net/RPT/PerformanceReview.aspx?format=Primary%20Sales&wise=P&DOC_TYPE=SS&RPT_HEADER=Monthly%20Sales-Summary&CBOYN=Y&FY_YEAR=2026-2027&COMPANY_CODE=DIOS&PA_ID=6958&DESIG_ID=1&DESIG=BE&PA_NAME=BANWARI%20LAL%20MEENA&HEAD_QTR=UDAIPUR&DIVISION_NAME=DIOS%20GROUP&FMCGYN=N&MENU_STYLE=NONE&ACTION_FROM=ANDROID&LOGIN_PA_ID=6958&LOGIN_COMPANY_ID=1"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
    context = browser.new_context(viewport={'width': 1440, 'height': 900})
    page = context.new_page()

    page.goto(LOGIN_URL, timeout=60000, wait_until="domcontentloaded")
    page.wait_for_timeout(1500)
    page.fill("input[type='text']", CBO_USER)
    page.fill("input[type='password']", CBO_PASS)
    page.keyboard.press("Enter")
    page.wait_for_timeout(3500)

    page.goto(DIRECT_REPORT_URL, timeout=60000, wait_until="domcontentloaded")
    page.wait_for_timeout(4000)

    # Let's call the endpoints directly in page context (which has the cookies)
    print("Testing GETDATAGRID & GETGROUPEDBYDATAGRID directly inside browser...")
    
    result = page.evaluate('''async () => {
        // 1. Call GETDATAGRID
        const gridPayload = {
            'LOGIN_PA_ID': '6958',
            'GROUPON': 'null',
            'WISE': 'null',
            'FMONTH': '08/01/2026',
            'TMONTH': '08/01/2026',
            'COLUMN': 'PRI_QTY,PRI_VAL',
            'DATEYN': '0',
            'GROUPFILTER': '0',
            'WISEFILTER': '0',
            'TARGET_ID': '0',
            'LRTYPE': 'V',
            'SPL_ID': '0',
            'STATE_ID': '0',
            'HQ_ID': '0',
            'ITEM_ID': '0',
            'ITEMG_ID': '0',
            'ITEM_HR': '0',
            'GROUP_COULUMN': '',
            'STK_ID': '0',
            'ITEM_STATUS': '1',
            'QTRWISE_TOTALYN': '0',
            'HORIZONTALYN': '0',
            'BILLYN': '0',
            'ITEM_HR_ZERO': '0',
            'STK_STATUS_P': '0',
            'STK_STATUS_S': '0',
            'SALE_SHARE': 'H',
            'iLYSALE_ON_CYTEAM': '1',
            'sADD_COL': '',
            'iPRI_PERIOD': '0',
            'iROUDATA': '0',
            'iOUTST_PERIOD': '0',
            'ITEMG_ID_2': '0',
            'ITEMG_ID_3': '0',
            'iOUTST_BALANCE': '0',
            'COMPANY_ID': '0',
            'CRM_HQ_GROUP_ID': '0',
            'ITEMG_ID_4': '0',
            'PARTY_GROUP': '0'
        };

        const res1 = await fetch('https://dios.myreporting.net/RPT/PerformanceReview.aspx/GETDATAGRID', {
            method: 'POST',
            headers: {'Content-Type': 'application/json; charset=UTF-8'},
            body: JSON.stringify(gridPayload)
        });
        const json1 = await res1.json();

        // 2. Call GETGROUPEDBYDATAGRID_1 with Product
        const res2 = await fetch('https://dios.myreporting.net/RPT/PerformanceReview.aspx/GETGROUPEDBYDATAGRID_1', {
            method: 'POST',
            headers: {'Content-Type': 'application/json; charset=UTF-8'},
            body: JSON.stringify({'GROUPCOLUMN': 'ITEM_NAME'})
        });
        const json2 = await res2.json();

        return { getdatagrid: json1, grouped: json2 };
    }''')

    print("Result 1 (GETDATAGRID):", str(result['getdatagrid'])[:200])
    print("Result 2 (Grouped by Item):", str(result['grouped'])[:500])

    with open('/workspaces/Dios/direct_api_result.json', 'w') as f:
        json.dump(result, f, indent=2)

    print("\n✅ Saved to direct_api_result.json")
    browser.close()
