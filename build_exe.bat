@echo off
pyinstaller --onefile  --hidden-import selenium  ablesci_auto_download.py
pause
