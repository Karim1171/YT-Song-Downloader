@echo off
pip install -U yt-dlp pyinstaller
pyinstaller --onefile --windowed --name YT-Song-Downloader --icon app_icon.ico --add-data "app_icon.ico;." --collect-all yt_dlp yt_song_downloader.py
pause
