#!/bin/bash

echo ""
echo "╔════════════════════════════════════════════════════╗"
echo "║   TikTok Video Enhancer 120 FPS - Mac/Linux        ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found!"
    echo "Install from: https://www.python.org/downloads/"
    exit 1
fi

echo "✅ Python3 found"
echo "Installing dependencies..."
pip3 install opencv-python numpy -q

echo ""
echo "Starting TikTok Video Enhancer..."
echo ""

python3 tiktok_enhancer.py
echo ""
read -p "Press Enter to exit..."
