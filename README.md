# YT-Song-Downloader

A simple Windows desktop app that downloads YouTube audio as MP3 (or M4A, Opus, FLAC, WAV) with the title, channel name, and thumbnail saved into the file.

## Download

Get the latest version here:
https://github.com/Karim1171/YT-Song-Downloader/releases/latest

## Features

- Paste any YouTube video or playlist link.
- Convert audio to MP3, M4A, Opus, FLAC, or WAV.
- Choose audio quality (0 is best, or 128 to 320 kbps).
- Automatically writes song titles and channel names into file tags.
- Embeds video thumbnails as album artwork.
- Remembers your chosen download folder for future downloads.
- Visual progress bar and live status log.

## Screenshot

Screenshot coming soon

## Requirements

- Windows 10 or 11.
- FFmpeg, required for conversion and tagging (needed for both options below).
- Python 3.10 or newer, only if you run from source. tkinter is included with the standard Windows installer.

To check if FFmpeg is already installed, open PowerShell or Command Prompt and run:
```powershell
ffmpeg -version
```
If you see version details, FFmpeg is installed. If Windows shows an error that the command is not recognized, install FFmpeg using the steps below.

## Installation

### Option A (Easiest)

Download `YT-Song-Downloader.exe` from the latest GitHub Release and double-click it. No Python needed.

Install FFmpeg first. Open PowerShell or Command Prompt and run:
```powershell
winget install ffmpeg
```
Restart the app after installing FFmpeg.

### Option B (From Source)

For people who want the Python code:

1. Install FFmpeg. Open PowerShell or Command Prompt and run:
```powershell
winget install ffmpeg
```
Restart the terminal after installing.

2. Download or clone this repository.

3. In the project folder, install the required Python packages:
```powershell
pip install -r requirements.txt
```

4. Run the app:
```powershell
python yt_song_downloader.py
```

## Building the .exe Yourself

Run `build_exe.bat`, or run this command manually from the project folder:
```powershell
pyinstaller --onefile --windowed --name YT-Song-Downloader --icon app_icon.ico --add-data "app_icon.ico;." --collect-all yt_dlp yt_song_downloader.py
```

The file appears at `dist\YT-Song-Downloader.exe`. FFmpeg must still be installed on the machine that runs the .exe.

## How to Use

1. Paste a YouTube video or playlist link into the URL field.
2. Choose your preferred audio format from the dropdown menu.
3. Choose your audio quality. Value 0 gives the best quality.
4. Choose an output folder with the Browse button, or type a path into the box.
5. Click Download.

Songs go to C:\Music the first time. Choose another folder with Browse, and the app will remember it for next time.

## Troubleshooting

- "FFmpeg not found": Install FFmpeg (run `winget install ffmpeg` in PowerShell or Command Prompt) and restart the app.
- Downloads fail: Run the following command and try again:
```powershell
pip install -U yt-dlp
```
YouTube changes often break older versions of yt-dlp. If you use the .exe, a newer release may be needed.
- Windows SmartScreen warning on the .exe: The app is not code-signed. Click "More info", then "Run anyway".
- Want to reset the default folder: Delete `%APPDATA%\YT-Song-Downloader\config.json`. The app will go back to C:\Music.

## Notes on Metadata

Titles may include text like "(Official Video)", and the artist field may only be the channel name.


## Credits

- Built on yt-dlp: https://github.com/yt-dlp/yt-dlp
- Audio processing with FFmpeg: https://ffmpeg.org


