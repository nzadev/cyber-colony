#!/bin/bash
# 🚀 Cyber Colony Tycoon - Auto Sync & Deploy Script
echo "=================================================="
echo "🔄 Menyiapkan sinkronisasi update ke Cloud..."
echo "=================================================="

cd "$(dirname "$0")"

MSG="${1:-Update sistem & optimasi gameplay $(date '+%d-%m-%Y %H:%M')}"
VER="${2:-v1.5.2}"
CAT="${3:-UPDATE}"

# Auto update changelog catalog & prune old entries (>14 days or >50 entries)
python3 update_changelog.py "$MSG" "$VER" "$CAT"

git add .
git commit -m "$MSG"

# Push to default branch
BRANCH=$(git branch --show-current 2>/dev/null || echo "main")
git push origin "$BRANCH"

echo ""
echo "✅ Push selesai ke branch '$BRANCH'!"
echo "🚀 Web GitHub Pages akan otomatis ter-update dalam 15-30 detik!"
echo "=================================================="
