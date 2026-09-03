#!/bin/bash
# ==============================================================================
# 🚀 PROTOCOL ZERO - 1-CLICK INSTANT WEB & APK DEPLOYER
# ==============================================================================

set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
ANDROID_DIR="$PROJECT_DIR/builds/android"

echo "=================================================="
echo "⚡ [1-CLICK DEPLOY] Protocol Zero Instant Push"
echo "=================================================="
echo "📦 1/3 Mengekspor APK Android terbaru..."

cd "$PROJECT_DIR"
godot --headless --export-release "Cyber Colony Tycoon" "$ANDROID_DIR/protocol_zero.apk" > /dev/null 2>&1 || true

cd "$ANDROID_DIR"
cp -f protocol_zero.apk protocol_zero_prototype.apk 2>/dev/null || true

echo "📝 2/3 Menyimpan perubahan & catatan update..."
git add .
git commit -m "Auto Update: $(date '+%d-%m-%Y %H:%M:%S')" 2>/dev/null || true

echo "⬆️ 3/3 Mengunggah langsung ke GitHub..."
git push origin main

echo ""
echo "=================================================="
echo "🎉 BERHASIL DI-PUSH DALAM 1 PERINTAH!"
echo "🌐 Web Live: https://nzadev.github.io/cyber-colony/"
echo "=================================================="
