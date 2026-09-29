#!/bin/bash

echo ""
echo "========================================"
echo "   اداة تحسين الفيديو الى جودة 8K"
echo "========================================"
echo ""

# التحقق من Python
if ! command -v python3 &> /dev/null; then
    echo "[X] Python3 غير مثبت!"
    echo "يرجى التثبيت باستخدام:"
    echo "  macOS: brew install python3"
    echo "  Linux: sudo apt install python3"
    exit 1
fi

echo "[✓] Python3 مثبت بنجاح"
echo ""

# التحقق من المكتبات
python3 -c "import cv2" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "[!] المتطلبات غير مثبتة، جاري التثبيت..."
    pip3 install -r requirements.txt
    echo "[✓] تم تثبيت المتطلبات"
    echo ""
fi

# تشغيل البرنامج
echo "[▶] جاري تشغيل البرنامج..."
echo ""
python3 enhance_video.py
