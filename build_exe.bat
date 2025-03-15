@echo off
pyinstaller --onefile  --hidden-import selenium --hidden-import webdriver_manager ablesci_auto_download.py
pause
