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
r_login_page = session.get("https://dios.myreporting.net/Login.aspx")
soup = BeautifulSoup(r_login_page.text, 'html.parser')

login_data = {
    "__VIEWSTATE": soup.find('input', {'name': '__VIEWSTATE'})['value'],
    "__VIEWSTATEGENERATOR": soup.find('input', {'name': '__VIEWSTATEGENERATOR'})['value'],
    "__EVENTVALIDATION": soup.find('input', {'name': '__EVENTVALIDATION'})['value'],
    "txtUserName": CBO_USER,
    "txtPassword": CBO_PASS,
    "btnLogin": "Login"
}
session.post("https://dios.myreporting.net/Login.aspx", data=login_data, allow_redirects=False)

# 2. Report Page Init
report_url = "https://dios.myreporting.net/RPT/PerformanceReview.aspx?format=Primary%20Sales&wise=P&DOC_TYPE=SS&RPT_HEADER=Monthly%20Sales-Summary&CBOYN=Y&FY_YEAR=2026-2027&COMPANY_CODE=DIOS&PA_ID=6958&DESIG_ID=1&DESIG=BE&PA_NAME=BANWARI%20LAL%20MEENA&HEAD_QTR=UDAIPUR&DIVISION_NAME=DIOS%20GROUP&FMCGYN=N&MENU_STYLE=NONE&ACTION_FROM=ANDROID&LOGIN_PA_ID=6958&LOGIN_COMPANY_ID=1"
session.get(report_url)

# 3. GETDATAGRID
grid_payload = {
    'LOGIN_PA_ID': '6958',
    'GROUPON': 'null',
    'WISE': 'null',
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

r_grid = session.post(
    "https://dios.myreporting.net/RPT/PerformanceReview.aspx/GETDATAGRID",
    json=grid_payload,
    headers={'Content-Type': 'application/json; charset=utf-8', 'X-Requested-With': 'XMLHttpRequest', 'Referer': report_url}
)

# 4. GETGROUPEDBYDATAGRID_1
drill_payload = {
    'GROUPCOLUMN': 'ITEM_NAME'
}
r_drill = session.post(
    "https://dios.myreporting.net/RPT/PerformanceReview.aspx/GETGROUPEDBYDATAGRID_1",
    json=drill_payload,
    headers={'Content-Type': 'application/json; charset=utf-8', 'X-Requested-With': 'XMLHttpRequest', 'Referer': report_url}
)
print("GETGROUPEDBYDATAGRID_1 Status:", r_drill.status_code)
raw_drill = r_drill.json().get('d', '')
if raw_drill:
    parsed = json.loads(raw_drill)
    for k, v in parsed.items():
        print(f"Table '{k}' count: {len(v)}")
        if len(v) > 0:
            print("Row 0:", v[0])
            print("Row 1:", v[1] if len(v)>1 else "")

# 5. Direct OpenExcel.aspx Download test
r_excel = session.get("https://dios.myreporting.net/RPT/OpenExcel.aspx?title=Monthly%20Sales-Summary")
print("\nOpenExcel.aspx Status:", r_excel.status_code, "Size:", len(r_excel.content))
if r_excel.status_code == 200 and len(r_excel.content) > 1000:
    with open('/workspaces/Dios/csv_output/Direct_CBO_Export.xls', 'wb') as f:
        f.write(r_excel.content)
    print("🎉 Direct Excel Downloaded & saved to csv_output/Direct_CBO_Export.xls!")
