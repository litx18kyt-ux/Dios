import requests, re

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})

print("🔍 Inspecting Angular Routing Table & ASPX endpoints in CBO...")
r = session.get("https://dios.myreporting.net/erp/main.351cc31a09a59193.js")
js = r.text

# 1. Search for any word ending with 'Report' or 'Stockist' or 'Cnf'
keywords = set(re.findall(r'["\']([a-zA-Z0-9_\/]*Cnf[a-zA-Z0-9_\/]*)["\']', js, re.IGNORECASE))
keywords.update(re.findall(r'["\']([a-zA-Z0-9_\/]*Stockist[a-zA-Z0-9_\/]*)["\']', js, re.IGNORECASE))
keywords.update(re.findall(r'["\']([a-zA-Z0-9_\/]*SPO[a-zA-Z0-9_\/]*)["\']', js, re.IGNORECASE))

print("\n--- MATCHING ROUTES / ENDPOINTS FOUND IN ANGULAR ---")
for kw in sorted(keywords):
    if len(kw) > 3 and not any(x in kw for x in [' ', '<', '>', '{', '}']):
        print("  ->", kw)

# 2. Search for Angular router paths
routes = set(re.findall(r'path:\s*["\']([^"\']+)["\']', js))
print(f"\n--- ANGULAR ROUTES (Total {len(routes)}) ---")
for route in sorted(routes):
    if any(k in route.lower() for k in ['report', 'sale', 'dcr', 'stock', 'cnf', 'spo']):
        print("  -> path:", route)
