#!/bin/bash
pkill -f uvicorn || true
echo "🚀 Starting CBO Python Engine on Port 8000..."
nohup uvicorn server:app --host 0.0.0.0 --port 8000 > /workspaces/Dios/server.log 2>&1 &
sleep 2

echo "🌐 Making Port 8000 Public..."
gh codespace ports visibility 8000:public -c $CODESPACE_NAME 2>/dev/null || true

echo ""
echo "========================================================"
echo "✅ CBO ENGINE IS NOW LIVE IN BACKGROUND!"
echo "Ab aap https://dios-hub.pages.dev par jakar 'Fetch & Auto-Fill Table' dabayein."
echo "========================================================"
