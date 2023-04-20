import os
import yt_dlp
import tkinter as tk
from tkinter import filedialog

class App:
    def __init__(self, master):
        self.master = master
        master.title("YouTube Audio Downloader")
        master.resizable(True, True)

        self.url_label = tk.Label(master, text="Enter the YouTube video/playlist URL:")
        self.url_label.pack()

        self.url_entry = tk.Entry(master, width=100)
        self.url_entry.pack(padx=10, pady=5)

        self.browse_button = tk.Button(master, text="Choose Output Directory", command=self.choose_directory)
        self.browse_button.pack(padx=10, pady=5)

        self.download_button = tk.Button(master, text="Download Audio", command=self.download_audio)
        self.download_button.pack(padx=10, pady=5)

        self.quit_button = tk.Button(master, text="Quit", command=master.quit)
        self.quit_button.pack(padx=10, pady=5)

        self.status_label = tk.Label(master, text="")
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
