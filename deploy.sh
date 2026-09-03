#!/bin/bash
# 🚀 Cyber Colony Tycoon - Auto Sync & Deploy Script
echo "=========================================="
echo "🔄 Menyiapkan sinkronisasi update ke Cloud..."
echo "=========================================="

cd "$(dirname "$0")"

git add .
MSG="${1:-Update website & game $(date '+%d-%m-%Y %H:%M')}"
git commit -m "$MSG"

# Push to default branch
BRANCH=$(git branch --show-current 2>/dev/null || echo "main")
git push origin "$BRANCH"

echo ""
echo "✅ Push selesai ke branch '$BRANCH'!"
echo "🚀 Server Cloud akan otomatis mendeteksi update & me-refresh web dalam 10-20 detik!"
echo "=========================================="
