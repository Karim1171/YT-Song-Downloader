# Release Notes - v1.0.0

## Overview

This is the initial release of YT-Song-Downloader, a simple desktop app for Windows that downloads audio from YouTube videos and playlists.

## What It Does

- Downloads audio in MP3, M4A, Opus, FLAC, or WAV format.
- Lets you select audio quality from 128 kbps up to best quality (0).
- Automatically writes the song title and channel name into the file metadata tags.
- Embeds the video thumbnail directly into the file as album artwork.
- Remembers your output folder. Songs go to C:\Music the first time the app runs. After that, the app remembers the last folder you chose in `%APPDATA%\YT-Song-Downloader\config.json`.

## Download & Setup

- Standalone Executable: Download `YT-Song-Downloader.exe` from the release assets below and run it directly without installing Python.
- FFmpeg Requirement: FFmpeg is required on your computer to convert audio formats and embed album art. Install it with:
```powershell
winget install ffmpeg
```
Restart the app after installing FFmpeg.

## Known Limits

- Titles may include video text like "(Official Video)" or "(Audio)".
- The artist field is set to the YouTube channel name, which might differ from the actual artist.
