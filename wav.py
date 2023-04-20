import os
import yt_dlp
import tkinter as tk
from tkinter import filedialog

class App:
    def __init__(self, master):
        self.master = master
        master.title("YouTube Audio Downloader")
        master.resizable(True, True)

        self.create_widgets()

    def create_widgets(self):
        self.create_url_entry()
        self.create_browse_button()
        self.create_download_button()
        self.create_quit_button()
        self.create_status_label()

    def create_url_entry(self):
        self.url_label = tk.Label(self.master, text="Enter the YouTube video/playlist URL:")
        self.url_label.pack()

        self.url_entry = tk.Entry(self.master, width=100)
        self.url_entry.pack(padx=10, pady=5)

    def create_browse_button(self):
        self.browse_button = tk.Button(self.master, text="Choose Output Directory", command=self.choose_directory)
        self.browse_button.pack(padx=10, pady=5)

    def create_download_button(self):
        self.download_button = tk.Button(self.master, text="Download Audio", command=self.download_audio)
        self.download_button.pack(padx=10, pady=5)

    def create_quit_button(self):
        self.quit_button = tk.Button(self.master, text="Quit", command=self.master.quit)
        self.quit_button.pack(padx=10, pady=5)

    def create_status_label(self):
        self.status_label = tk.Label(self.master, text="")
        self.status_label.pack()

    def choose_directory(self):
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.output_dir = dir_path
            self.status_label.config(text=f"Output directory: {self.output_dir}")

    def download_audio(self):
        video_url = self.url_entry.get()
        if not video_url:
            self.status_label.config(text="Error: Enter a valid YouTube URL")
            return

        if not hasattr(self, 'output_dir'):
            self.status_label.config(text="Error: Choose an output directory")
            return

        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(self.output_dir, '%(title)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'wav',
                    'preferredquality': '192',
                }],
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(video_url, download=True)
                if 'entries' in info_dict:
                    # Playlist
                    for entry in info_dict['entries']:
                        file_path = ydl.prepare_filename(entry)
                        self.status_label.config(text=f"Successfully downloaded audio file: {os.path.splitext(file_path)[0]}.wav")
                else:
                    # Single video
                    file_path = ydl.prepare_filename(info_dict)
                    self.status_label.config(text=f"Successfully downloaded audio file: {os.path.splitext(file_path)[0]}.wav")
        except Exception as e:
            self.status_label.config(text=f"Error: {e}")

root = tk.Tk()
app = App(root)
root.mainloop()
