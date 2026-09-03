#!/bin/bash
cd "$(dirname "$0")"

echo "=================================================="
echo "🚀 Cyber Colony Tycoon - GitHub Push Helper"
echo "=================================================="
echo ""
echo "Silakan masukkan Token GitHub Anda (yang diawali ghp_...)"
read -p "👉 Paste Token di sini: " USER_TOKEN

if [ -z "$USER_TOKEN" ]; then
    echo "❌ Token tidak boleh kosong!"
    exit 1
fi

# Set remote with token
echo ""
echo "🔄 Menghubungkan ke repository GitHub..."
git remote set-url origin "https://${USER_TOKEN}@github.com/nzadev/cyber-colony.git"

echo "⬆️ Mengunggah file ke GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "=================================================="
    echo "🎉 BERHASIL DI-PUSH KE GITHUB!"
    echo "Sekarang Anda bisa buka dashboard.render.com untuk mengaktifkan web 24/7!"
    echo "=================================================="
else
    echo ""
    echo "❌ Push gagal. Mohon pastikan token benar dan memiliki centang 'repo'."
fi
