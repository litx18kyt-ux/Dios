import requests, re

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})

print("Downloading CBO frontend JS bundle...")
r = session.get("https://dios.myreporting.net/erp/main.351cc31a09a59193.js")
js_code = r.text
print("JS length:", len(js_code))

# Search for /api/token in JS
token_matches = [m.start() for m in re.finditer(r'/api/token', js_code)]
print(f"Found {len(token_matches)} occurrences of /api/token")

for pos in token_matches:
    start = max(0, pos - 400)
    end = min(len(js_code), pos + 400)
    print("\n--- CODE SNIPPET AROUND /api/token ---")
    print(js_code[start:end])

