#!/bin/bash
cd "$(dirname "$0")"
echo "======================================================="
echo " 👑 WINNING HEAVEN EMAIL MARKETING APPLICATION"
echo "======================================================="
echo "Opening Dashboard in your browser..."
python3 -c "import time, webbrowser; time.sleep(1); webbrowser.open('http://127.0.0.1:5050')" &
python3 app.py
