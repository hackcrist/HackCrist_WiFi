#!/bin/bash
# HackCrist WiFi Audit Script Installer

clear
echo "🚀 HackCrist WiFi Audit Script - Installer"

echo "[+] Updating packages..."
pkg update -y && pkg upgrade -y

echo "[+] Installing Python and pip..."
pkg install python -y

echo "[+] Installing pywifi..."
pip install pywifi

echo "[+] Installation complete!"
echo "[+] Opening TikTok channel..."

if [[ $PREFIX == *"com.termux"* ]]; then
  termux-open-url "https://www.tiktok.com/@ethicalcore?_t=ZT-8xeJ7JR4paQ&_r=1"
else
  xdg-open "https://www.tiktok.com/@ethicalcore?_t=ZT-8xeJ7JR4paQ&_r=1"
fi

echo "[+] Follow my TikTok @ethicalcore ❤️"
