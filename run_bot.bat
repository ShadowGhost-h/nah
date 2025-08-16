@echo off
title Yami no Sekai Discord Bot
echo 🔄 Đang chạy bot với auto-reload bằng watchdog...
watchmedo auto-restart --patterns="*.py" --recursive -- python bot.py
pause
