#!/bin/bash
cd "$(dirname "$0")"

echo "=================================================="
echo "🚀 Protocol Zero - GitHub Push & Auto-Sync Helper"
echo "=================================================="
echo ""

# Auto update changelog catalog & prune old entries (>14 days or >50 entries)
python3 update_changelog.py "Auto sync commit $(date '+%d-%m-%Y %H:%M')" "v1.5.2" "UPDATE"

git add .
git commit -m "Auto sync update catalog & builds" 2>/dev/null || true

echo "Silakan masukkan Token GitHub Anda (yang diawali ghp_...)"
read -p "👉 Paste Token di sini: " USER_TOKEN

if [ -z "$USER_TOKEN" ]; then
    echo "❌ Token tidak boleh kosong!"
    exit 1
fi

# Set remote with token
echo ""
echo "🔄 Menghubungkan ke repository GitHub nzadev/cyber-colony..."
git remote set-url origin "https://${USER_TOKEN}@github.com/nzadev/cyber-colony.git"

echo "⬆️ Mengunggah file ke GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "=================================================="
    echo "🎉 BERHASIL DI-PUSH KE GITHUB!"
    echo "Web di https://nzadev.github.io/cyber-colony/ akan otomatis ter-update dalam 20 detik!"
    echo "=================================================="
else
    echo ""
    echo "❌ Push gagal. Mohon pastikan token benar dan memiliki centang 'repo'."
fi
