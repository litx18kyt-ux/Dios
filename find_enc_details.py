import requests, re

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})

for fname in ["scripts.4bc6f945a9bc7b44.js", "main.351cc31a09a59193.js", "runtime.c9a57e747d776efc.js"]:
    url = f"https://dios.myreporting.net/erp/{fname}"
    r = session.get(url)
    print(f"File {fname} ({len(r.text)} bytes):")
    
    # Search for token, encrypt, grant_type
    for term in ["grant_type", "api/token", "encrypt", "btoa"]:
        matches = [m.start() for m in re.finditer(term, r.text, re.IGNORECASE)]
        if matches:
            print(f"  Found '{term}': {len(matches)} times")
            pos = matches[0]
            snippet = r.text[max(0, pos-100):min(len(r.text), pos+200)]
            print(f"  Snippet: {snippet}\n")
