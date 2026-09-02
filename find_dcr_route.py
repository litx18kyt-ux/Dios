import requests, re, json

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})

print("🔍 Searching for 'Date Wise Call Detail' in CBO JS Bundle...")
r = session.get("https://dios.myreporting.net/erp/main.351cc31a09a59193.js")
js_code = r.text

matches = [m.start() for m in re.finditer(r'Date Wise Call Detail', js_code, re.IGNORECASE)]
print(f"Found {len(matches)} occurrences.")

for pos in matches:
    start = max(0, pos - 200)
    end = min(len(js_code), pos + 300)
    print("\n--- CODE SNIPPET ---")
    print(js_code[start:end])

# Also search for RPT/ or .aspx related to DCR
aspx_matches = set(re.findall(r'RPT/[a-zA-Z0-9_\.]+\.aspx', js_code, re.IGNORECASE))
print("\n--- ALL RPT .aspx URLs FOUND ---")
for url in sorted(aspx_matches):
    print(" ->", url)
