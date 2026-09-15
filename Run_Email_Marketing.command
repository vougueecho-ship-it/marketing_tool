#!/bin/bash
cd "$(dirname "$0")"
# Free port 5050 if already in use
lsof -ti:5050 | xargs kill -9 2>/dev/null || true
echo "======================================================="
echo " 👑 WINNING HEAVEN EMAIL MARKETING APPLICATION"
echo "======================================================="
echo "Opening Dashboard in your browser..."
python3 -c "import time, webbrowser; time.sleep(1); webbrowser.open('http://127.0.0.1:5050')" &
python3 app.py
