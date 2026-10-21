import json
import os
import queue
import shutil
import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

import yt_dlp

FORMATS = ["mp3", "m4a", "opus", "flac", "wav"]
QUALITIES = ["0", "320", "256", "192", "128"]  # kbps, 0 = best

CONFIG_DIR = Path(os.environ.get("APPDATA", Path.home())) / "YT-Song-Downloader"
CONFIG_FILE = CONFIG_DIR / "config.json"
DEFAULT_FOLDER = Path("C:/Music")


def get_default_folder() -> str:
    """Return the saved folder from config.json, or C:/Music on first run."""
    if CONFIG_FILE.is_file():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                saved = data.get("output_folder")
                if saved:
                    return str(saved)
        except Exception:
            pass
    return str(DEFAULT_FOLDER)


def save_default_folder(folder_path: str):
    """Save the chosen output folder into config.json."""
    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump({"output_folder": folder_path}, f, indent=2)
    except Exception:
        pass


class App:
    def __init__(self, root):
        self.root = root
        root.title("YT Song Downloader")
        root.geometry("680x520")
        self.msgs = queue.Queue()

        # Warn if FFmpeg is missing on startup
        if not shutil.which("ffmpeg"):
            messagebox.showwarning(
                "FFmpeg Not Found",
                "FFmpeg was not found on your system.\n\n"
                "FFmpeg is required for converting and tagging songs. "
                "Please install FFmpeg (for example, run 'winget install ffmpeg') "
                "and restart the app.",
            )

        frm = ttk.Frame(root, padding=12)
        frm.pack(fill="both", expand=True)

        ttk.Label(frm, text="YouTube URL (video or playlist):").pack(anchor="w")
        self.url = ttk.Entry(frm)
        self.url.pack(fill="x", pady=(0, 8))

        row = ttk.Frame(frm)
        row.pack(fill="x", pady=(0, 8))
        ttk.Label(row, text="Format:").pack(side="left")
        self.fmt = ttk.Combobox(row, values=FORMATS, state="readonly", width=8)
        self.fmt.set("mp3")
        self.fmt.pack(side="left", padx=(4, 16))
        ttk.Label(row, text="Quality (kbps, 0 = best):").pack(side="left")
        self.quality = ttk.Combobox(row, values=QUALITIES, width=6)
        self.quality.set("0")
        self.quality.pack(side="left", padx=4)

        row2 = ttk.Frame(frm)
        row2.pack(fill="x", pady=(0, 8))
        self.outdir = tk.StringVar(value=get_default_folder())
        ttk.Entry(row2, textvariable=self.outdir).pack(side="left", fill="x", expand=True)
        ttk.Button(row2, text="Browse", command=self.pick_dir).pack(side="left", padx=4)

        self.btn = ttk.Button(frm, text="Download", command=self.start)
        self.btn.pack(pady=4)
        self.status = ttk.Label(frm, text="Idle")
        self.status.pack(anchor="w")
        self.progress = ttk.Progressbar(frm, mode="determinate", maximum=100)
        self.progress.pack(fill="x", pady=4)

        self.log = tk.Text(frm, height=12, state="disabled")
        self.log.pack(fill="both", expand=True)

        root.after(100, self.poll)

    def pick_dir(self):
        d = filedialog.askdirectory(initialdir=self.outdir.get())
        if d:
            self.outdir.set(d)
            save_default_folder(d)

    def log_line(self, text):
        self.log.configure(state="normal")
        self.log.insert("end", text + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def start(self):
        url = self.url.get().strip()
        if not url:
            messagebox.showwarning("Missing URL", "Paste a YouTube link first.")
            return
        folder = self.outdir.get().strip()
        if not folder:
            messagebox.showwarning("Missing folder", "Choose a folder to save to.")
            return
        save_default_folder(folder)
        fmt = self.fmt.get()
        quality = self.quality.get()
        self.btn.configure(state="disabled")
        self.progress["value"] = 0
        threading.Thread(
            target=self.worker, args=(url, folder, fmt, quality), daemon=True
        ).start()

    def hook(self, d):
        # Runs in the worker thread, so it only queues messages for the UI.
        if d["status"] == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate")
            if total:
                self.msgs.put(("progress", d.get("downloaded_bytes", 0) / total * 100))
            self.msgs.put(("status", f"Downloading {d.get('_percent_str', '').strip()}"))
        elif d["status"] == "finished":
            title = d.get("info_dict", {}).get("title", "track")
            self.msgs.put(("log", f"Downloaded: {title}"))
            self.msgs.put(("status", "Converting and tagging..."))

    def worker(self, url, folder, fmt, quality):
        out = Path(folder)
        out.mkdir(parents=True, exist_ok=True)
        opts = {
            "format": "bestaudio/best",
            "outtmpl": str(out / "%(title)s.%(ext)s"),
            "writethumbnail": True,
            "progress_hooks": [self.hook],
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": fmt,
                    "preferredquality": quality,
                },
                {"key": "FFmpegMetadata", "add_metadata": True},
                {"key": "EmbedThumbnail"},
            ],
            "quiet": True,
            "no_warnings": True,
        }
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([url])
            self.msgs.put(("done", "Finished."))
        except Exception as e:
            self.msgs.put(("error", f"Error: {e}"))

    def poll(self):
        try:
            while True:
                kind, value = self.msgs.get_nowait()
                if kind == "progress":
                    self.progress["value"] = value
                elif kind == "status":
                    self.status.configure(text=value)
                elif kind == "log":
                    self.log_line(value)
                elif kind in ("done", "error"):
                    self.status.configure(text=value)
                    self.log_line(value)
                    self.progress["value"] = 100 if kind == "done" else 0
                    self.btn.configure(state="normal")
        except queue.Empty:
            pass
        self.root.after(100, self.poll)


def resource_path(name):
    """Find a bundled file both when running the script and inside the .exe."""
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    return base / name


if __name__ == "__main__":
    root = tk.Tk()
    icon_path = resource_path("app_icon.ico")
    if icon_path.exists():
        try:
            root.iconbitmap(str(icon_path))
        except Exception:
            pass
    App(root)
    root.mainloop()
