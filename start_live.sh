#!/bin/bash
set -e
cd /workspaces/Dios

echo "========================================================"
echo "🚀 1. Starting Python CBO Engine on Port 8000..."
echo "========================================================"
pkill -f uvicorn || true
sleep 1
nohup python3 -m uvicorn server:app --host 0.0.0.0 --port 8000 > /workspaces/Dios/server.log 2>&1 &
sleep 2

echo "========================================================"
echo "🌐 2. Setting Port 8000 to Public..."
echo "========================================================"
gh codespace ports visibility 8000:public -c $CODESPACE_NAME 2>/dev/null || true

PUBLIC_API="https://${CODESPACE_NAME}-8000.app.github.dev"
echo "Active Backend URL: $PUBLIC_API"

echo "========================================================"
echo "⚡ 3. Linking Cloudflare Bridge to this Codespace..."
echo "========================================================"
cat << CFEOF > functions/api/fetch-primary.ts
export async function onRequest(context: any) {
  if (context.request.method === "OPTIONS") {
    return new Response(null, {
      status: 204,
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization",
      },
    });
  }
  try {
    const body = await context.request.json();
    const apiRes = await fetch("${PUBLIC_API}/api/fetch-primary", {
      method: "POST",
      headers: { "Content-Type": "application/json", "Accept": "application/json" },
      body: JSON.stringify(body),
    });
    const data = await apiRes.text();
    return new Response(data, {
      status: apiRes.status,
      headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" },
    });
  } catch (err: any) {
    return new Response(JSON.stringify({
      success: false,
      error: "Connection error: " + (err.message || String(err))
    }), {
      status: 502,
      headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" },
    });
  }
}
CFEOF

cat << CFEOF2 > functions/api/fetch-cbo-excel.ts
export async function onRequest(context: any) {
  if (context.request.method === "OPTIONS") {
    return new Response(null, {
      status: 204,
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization",
      },
    });
  }
  try {
    const body = await context.request.json();
    const apiRes = await fetch("${PUBLIC_API}/api/fetch-cbo-excel", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const blob = await apiRes.arrayBuffer();
    return new Response(blob, {
      status: apiRes.status,
      headers: { "Content-Type": "application/vnd.ms-excel", "Access-Control-Allow-Origin": "*" },
    });
  } catch (err: any) {
    return new Response(JSON.stringify({
      success: false,
      error: "Download error: " + (err.message || String(err))
    }), {
      status: 502,
      headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" },
    });
  }
}
CFEOF2

echo "========================================================"
echo "☁️ 4. Building & Deploying to Cloudflare..."
echo "========================================================"
npm run build
npx wrangler pages deploy dist --project-name=dios-hub --branch=main --commit-dirty=true

echo ""
echo "========================================================"
echo "🎉 ALL DONE! SYSTEM IS FULLY LIVE & SYNCED!"
echo "👉 Open: https://dios-hub.pages.dev"
echo "========================================================"
