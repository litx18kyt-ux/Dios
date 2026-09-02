import requests, re

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})

# Download the main JS bundles of CBO
scripts = [
    "https://dios.myreporting.net/erp/main.351cc31a09a59193.js",
    "https://dios.myreporting.net/erp/scripts.4bc6f945a9bc7b44.js",
    "https://dios.myreporting.net/erp/runtime.c9a57e747d776efc.js"
]

print("🔍 Searching for 'CnfSpoStk_Report' in all CBO JS bundles...")
for s_url in scripts:
    name = s_url.split('/')[-1]
    print(f"Checking {name}...")
    r = session.get(s_url)
    text = r.text
    matches = [m.start() for m in re.finditer(r'CnfSpoStk_Report', text, re.IGNORECASE)]
    if matches:
        print(f"🔥 FOUND in {name}: {len(matches)} times!")
        for pos in matches:
            start = max(0, pos - 300)
            end = min(len(text), pos + 300)
            print("\n--- EXACT CODE SNIPPET ---")
            print(text[start:end])
            print("--------------------------\n")
