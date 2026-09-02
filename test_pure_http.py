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

print("[1] Logging into CBO via HTTP...")
login_url = "https://dios.myreporting.net/Login.aspx"
r_get = session.get(login_url)
soup = BeautifulSoup(r_get.text, 'html.parser')

def get_val(soup, input_id):
    el = soup.find('input', {'id': input_id})
    return el.get('value', '') if el else ''

payload = {
    "__VIEWSTATE": get_val(soup, "__VIEWSTATE"),
    "__VIEWSTATEGENERATOR": get_val(soup, "__VIEWSTATEGENERATOR"),
    "__EVENTVALIDATION": get_val(soup, "__EVENTVALIDATION"),
    "txtUserName": CBO_USER,
    "txtPassword": CBO_PASS,
    "btnLogin": "Login"
}

r_post = session.post(login_url, data=payload, allow_redirects=False)
print("Login status:", r_post.status_code)

print("[2] Opening Report Page...")
report_url = f"https://dios.myreporting.net/RPT/PerformanceReview.aspx?format=Primary%20Sales&wise=P&DOC_TYPE=SS&RPT_HEADER=Monthly%20Sales-Summary&CBOYN=Y&FY_YEAR={FY_TARGET}&COMPANY_CODE=DIOS&PA_ID=6958&DESIG_ID=1&DESIG=BE&PA_NAME=BANWARI%20LAL%20MEENA&HEAD_QTR=UDAIPUR&DIVISION_NAME=DIOS%20GROUP&FMCGYN=N&MENU_STYLE=NONE&ACTION_FROM=ANDROID&LOGIN_PA_ID=6958&LOGIN_COMPANY_ID=1"
r_rep = session.get(report_url)
print("Report GET status:", r_rep.status_code)

soup_rep = BeautifulSoup(r_rep.text, 'html.parser')
# Find values for Aug-2026 in MFDATE/MTDATE
mfdate_val = ""
mtdate_val = ""
for sel in soup_rep.find_all('select'):
    s_id = (sel.get('id') or '').upper()
    if 'FDATE' in s_id or 'TDATE' in s_id:
        for opt in sel.find_all('option'):
            if MONTH_TARGET.lower() in opt.text.lower() or MONTH_TARGET[:3].lower() in opt.text.lower():
                if 'FDATE' in s_id: mfdate_val = opt.get('value', '')
                if 'TDATE' in s_id: mtdate_val = opt.get('value', '')

form_data = {
    "__VIEWSTATE": get_val(soup_rep, "__VIEWSTATE"),
    "__VIEWSTATEGENERATOR": get_val(soup_rep, "__VIEWSTATEGENERATOR"),
    "__EVENTVALIDATION": get_val(soup_rep, "__EVENTVALIDATION"),
    "MFDATE": mfdate_val or MONTH_TARGET,
    "MTDATE": mtdate_val or MONTH_TARGET,
    "MGROUPING_ID": "0",
    "MDDLSUMMARY": "0",
    "MSTAFF_TYPE": "1",
    "MPA_ID": "6958",
    "btnGo": "Go"
}

print(f"[3] Submitting Date Filter ({MONTH_TARGET})...")
r_submit = session.post(report_url, data=form_data)
print("Filter Submit Status:", r_submit.status_code)

print("[4] Fetching Product List via AJAX GETGROUPEDBYDATAGRID_1...")
ajax_url = "https://dios.myreporting.net/RPT/PerformanceReview.aspx/GETGROUPEDBYDATAGRID_1"
headers = {
    "Content-Type": "application/json; charset=UTF-8",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": report_url
}
r_ajax = session.post(ajax_url, json={"GROUPCOLUMN": "Product"}, headers=headers)
print("AJAX Status:", r_ajax.status_code)
try:
    data = r_ajax.json()
    parsed_table = json.loads(data['d'])
    for table_name, rows in parsed_table.items():
        print(f"🎉 SUCCESS! Found table '{table_name}' with {len(rows)} items:")
        for row in rows[:5]:
            print("  •", row)
except Exception as e:
    print("Error parsing AJAX response:", e)
    print("Raw text:", r_ajax.text[:400])
