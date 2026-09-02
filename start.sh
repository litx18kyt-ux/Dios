#!/bin/bash
pkill -f uvicorn || true
echo "🚀 Starting Python CBO API Server on port 8000..."
nohup uvicorn server:app --host 0.0.0.0 --port 8000 > server.log 2>&1 &

echo "✨ Starting Vite Frontend..."
npm run dev
