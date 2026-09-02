import requests, json
from bs4 import BeautifulSoup

CBO_USER = "6958BANWARI"
CBO_PASS = "6958"

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
})

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

report_url = "https://dios.myreporting.net/RPT/PerformanceReview.aspx?format=Primary%20Sales&wise=P&DOC_TYPE=SS&RPT_HEADER=Monthly%20Sales-Summary&CBOYN=Y&FY_YEAR=2026-2027&COMPANY_CODE=DIOS&PA_ID=6958&DESIG_ID=1&DESIG=BE&PA_NAME=BANWARI%20LAL%20MEENA&HEAD_QTR=UDAIPUR&DIVISION_NAME=DIOS%20GROUP&FMCGYN=N&MENU_STYLE=NONE&ACTION_FROM=ANDROID&LOGIN_PA_ID=6958&LOGIN_COMPANY_ID=1"
r_rep = session.get(report_url)

# Search all javascript functions and WebMethods in the HTML
soup_rep = BeautifulSoup(r_rep.text, 'html.parser')
scripts = [s.text for s in soup_rep.find_all('script') if s.text]
all_js = "\n".join(scripts)

# Find all ajax url calls
import re
ajax_calls = set(re.findall(r'url:\s*["\']([^"\']+)["\']', all_js, re.IGNORECASE))
print("Available AJAX URLs on page:")
for call in ajax_calls:
    print(" ->", call)

# Also check if there is an external js file like PerformanceReview.js or similar
js_srcs = [s.get('src') for s in soup_rep.find_all('script') if s.get('src')]
print("\nJS Files loaded:")
for src in js_srcs:
    print(" ->", src)
