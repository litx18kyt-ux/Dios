#!/bin/bash
set -e

if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

echo "🚀 1. Building Vite project..."
npm run build

echo "☁️ 2. Deploying to Cloudflare Production..."
npx wrangler pages deploy dist --project-name=dios-hub --branch=main --commit-dirty=true

echo ""
echo "========================================================"
echo "✅ DEPLOYMENT FINISHED!"
echo "🌐 OPEN THIS URL IN BROWSER: https://dios-hub.pages.dev"
echo "========================================================"
