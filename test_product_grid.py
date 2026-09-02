import requests, json
from bs4 import BeautifulSoup

CBO_USER = "6958BANWARI"
CBO_PASS = "6958"
MONTH_TARGET = "08/01/2026"

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
})

# 1. Login
r_get = session.get("https://dios.myreporting.net/Login.aspx")
soup = BeautifulSoup(r_get.text, 'html.parser')

def get_field(soup, name):
    el = soup.find('input', {'name': name})
    return el.get('value', '') if el else ''

login_data = {
    "__VIEWSTATE": get_field(soup, "__VIEWSTATE"),
    "__VIEWSTATEGENERATOR": get_field(soup, "__VIEWSTATEGENERATOR"),
    "__EVENTVALIDATION": get_field(soup, "__EVENTVALIDATION"),
    "txtUserName": CBO_USER,
    "txtPassword": CBO_PASS,
    "btnLogin": "Login"
}
session.post("https://dios.myreporting.net/Login.aspx", data=login_data, allow_redirects=False)

# 2. Report page
report_url = "https://dios.myreporting.net/RPT/PerformanceReview.aspx?format=Primary%20Sales&wise=P&DOC_TYPE=SS&RPT_HEADER=Monthly%20Sales-Summary&CBOYN=Y&FY_YEAR=2026-2027&COMPANY_CODE=DIOS&PA_ID=6958&DESIG_ID=1&DESIG=BE&PA_NAME=BANWARI%20LAL%20MEENA&HEAD_QTR=UDAIPUR&DIVISION_NAME=DIOS%20GROUP&FMCGYN=N&MENU_STYLE=NONE&ACTION_FROM=ANDROID&LOGIN_PA_ID=6958&LOGIN_COMPANY_ID=1"
session.get(report_url)

# 3. Test different WISE / GROUPON combinations for product list
for groupon, wise, col_name in [('P', 'null', 'ITEM_NAME'), ('null', 'P', 'ITEM_NAME'), ('null', 'null', 'ITEM_NAME'), ('I', 'null', 'ITEM_NAME'), ('null', 'null', 'Product')]:
    grid_payload = {
        'LOGIN_PA_ID': '6958',
        'GROUPON': groupon,
        'WISE': wise,
        'FMONTH': MONTH_TARGET,
        'TMONTH': MONTH_TARGET,
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
    }

    session.post("https://dios.myreporting.net/RPT/PerformanceReview.aspx/GETDATAGRID", json=grid_payload, headers={'Content-Type':'application/json; charset=utf-8'})
    r_sub = session.post("https://dios.myreporting.net/RPT/PerformanceReview.aspx/GETGROUPEDBYDATAGRID_1", json={'GROUPCOLUMN': col_name}, headers={'Content-Type':'application/json; charset=utf-8'})
    
    try:
        data = r_sub.json().get('d', '')
        if data:
            parsed = json.loads(data)
            tbl = parsed.get('Table', [])
            print(f"Test (GROUPON={groupon}, WISE={wise}, col={col_name}) -> Got {len(tbl)} rows")
            if len(tbl) > 1:
                print("🎉 SUCCESS! Sample row:", tbl[0])
                break
    except Exception as e:
        print("Error:", e)
