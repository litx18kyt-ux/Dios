#!/bin/bash
echo "🚀 Starting Python CBO API Server on port 8000..."
uvicorn server:app --host 0.0.0.0 --port 8000 &

echo "✨ Starting Vite Frontend..."
npm run dev
