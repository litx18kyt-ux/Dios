#!/bin/bash
cd /workspaces/Dios

echo "========================================================"
echo "🚀 STARTING DIOS UNIFIED BACKEND SERVER (PORT 8000)..."
echo "========================================================"

pkill -f uvicorn || true
sleep 1

nohup python3 -m uvicorn server:app --host 0.0.0.0 --port 8000 > /workspaces/Dios/server.log 2>&1 &
sleep 2

gh codespace ports visibility 8000:public -c "${CODESPACE_NAME:-redesigned-winner-gx7rv659g97vhp7r9}" 2>/dev/null || true

CHECK=$(curl -s http://127.0.0.1:8000/ || echo "OFFLINE")

if [[ "$CHECK" == *"online"* ]]; then
  echo "✅ SERVER IS 100% LIVE & ACTIVE!"
  echo "📡 Version: v61.0 (All 4 Engines Unified)"
  echo "🌐 Public URL: https://${CODESPACE_NAME:-redesigned-winner-gx7rv659g97vhp7r9}-8000.app.github.dev"
  echo "========================================================"
else
  echo "❌ Error starting server. server.log:"
  cat /workspaces/Dios/server.log | tail -n 10
  echo "========================================================"
fi
