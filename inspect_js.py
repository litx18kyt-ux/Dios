import requests, re
from bs4 import BeautifulSoup

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})

# Login
r_get = session.get("https://dios.myreporting.net/Login.aspx")
soup = BeautifulSoup(r_get.text, 'html.parser')
login_data = {
    "__VIEWSTATE": soup.find('input', {'name': '__VIEWSTATE'})['value'],
    "__VIEWSTATEGENERATOR": soup.find('input', {'name': '__VIEWSTATEGENERATOR'})['value'],
    "__EVENTVALIDATION": soup.find('input', {'name': '__EVENTVALIDATION'})['value'],
    "txtUserName": "6958BANWARI", "txtPassword": "6958", "btnLogin": "Login"
}
session.post("https://dios.myreporting.net/Login.aspx", data=login_data, allow_redirects=False)

# Fetch PerformanceReviewDET.html
r_det = session.get("https://dios.myreporting.net/RPT/PerformanceReviewDET.html?v=26")
print("PerformanceReviewDET.html status:", r_det.status_code)
methods = re.findall(r'PerformanceReview\.aspx/\w+', r_det.text)
print("Found WebMethods in DET.html:", set(methods))

# Search for drilldown / click functions in DET.html
functions = re.findall(r'function\s+([a-zA-Z0-9_]+)\s*\(', r_det.text)
print("\nJS Functions found:", functions[:15])

with open('/workspaces/Dios/det_script.js', 'w', encoding='utf-8') as f:
    f.write(r_det.text)
print("\nSaved full script to det_script.js")
