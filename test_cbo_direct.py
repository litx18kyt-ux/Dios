import requests, json
from bs4 import BeautifulSoup

CBO_USER = "6958BANWARI"
CBO_PASS = "6958"
MONTH_TARGET = "Aug-2026"
FY_TARGET = "2026-2027"

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
})

print("[1] Logging in...")
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

r_login = session.post("https://dios.myreporting.net/Login.aspx", data=login_data, allow_redirects=False)
print("Login status:", r_login.status_code)

print("[2] Initializing Report Page...")
report_url = f"https://dios.myreporting.net/RPT/PerformanceReview.aspx?format=Primary%20Sales&wise=P&DOC_TYPE=SS&RPT_HEADER=Monthly%20Sales-Summary&CBOYN=Y&FY_YEAR={FY_TARGET}&COMPANY_CODE=DIOS&PA_ID=6958&DESIG_ID=1&DESIG=BE&PA_NAME=BANWARI%20LAL%20MEENA&HEAD_QTR=UDAIPUR&DIVISION_NAME=DIOS%20GROUP&FMCGYN=N&MENU_STYLE=NONE&ACTION_FROM=ANDROID&LOGIN_PA_ID=6958&LOGIN_COMPANY_ID=1"
r_rep = session.get(report_url)
print("Report GET status:", r_rep.status_code)

soup_rep = BeautifulSoup(r_rep.text, 'html.parser')

mfdate_val = ""
mtdate_val = ""
for sel in soup_rep.find_all('select'):
    s_name = (sel.get('name') or '').upper()
    if 'FDATE' in s_name or 'TDATE' in s_name:
        for opt in sel.find_all('option'):
            if "aug" in opt.text.lower():
                if 'FDATE' in s_name: mfdate_val = opt.get('value', '')
                if 'TDATE' in s_name: mtdate_val = opt.get('value', '')

print(f"Detected Date Values: FDATE={mfdate_val}, TDATE={mtdate_val}")

print("[3] Fetching Grid via AJAX...")
grid_payload = {
    'LOGIN_PA_ID': '6958',
    'GROUPON': 'null',
    'WISE': 'null',
    'FMONTH': mfdate_val or '08/01/2026',
    'TMONTH': mtdate_val or '08/01/2026',
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

r_grid = session.post("https://dios.myreporting.net/RPT/PerformanceReview.aspx/GETDATAGRID", json=grid_payload, headers={'Content-Type':'application/json; charset=utf-8'})
print("GETDATAGRID Status:", r_grid.status_code)

for col in ['ITEM_NAME', 'Product', 'HEAD_QTR']:
    r_sub = session.post("https://dios.myreporting.net/RPT/PerformanceReview.aspx/GETGROUPEDBYDATAGRID_1", json={'GROUPCOLUMN': col}, headers={'Content-Type':'application/json; charset=utf-8'})
    data = r_sub.json().get('d', '')
    if len(data) > 0:
        parsed = json.loads(data)
        tbl = parsed.get('Table', [])
        print(f"Group '{col}' returned {len(tbl)} items.")
        if len(tbl) > 0:
            print("   Sample:", tbl[0])
