import os
import tkinter as tk
import yt_dlp


class AudioDownloaderGUI:
    def __init__(self, master):
        self.master = master
        master.title("Audio Downloader")

        # URL input label and entry field
        self.url_label = tk.Label(master, text="YouTube video/playlist URL:")
        self.url_label.pack()
        self.url_entry = tk.Entry(master)
        self.url_entry.pack()

        # Output directory input label and entry field
        self.dir_label = tk.Label(master, text="Output directory:")
        self.dir_label.pack()
        self.dir_entry = tk.Entry(master)
        self.dir_entry.pack()

        # Download button
        self.download_button = tk.Button(master, text="Download", command=self.download)
        self.download_button.pack()

        # Status label
        self.status_label = tk.Label(master, text="")
        self.status_label.pack()

    def download(self):
        video_url = self.url_entry.get()
        output_dir = self.dir_entry.get()

        try:
            os.makedirs(output_dir, exist_ok=True)
            audio_file_path = download_audio(video_url, output_dir)
            self.status_label.configure(text=f"Successfully downloaded audio file: {audio_file_path}")
        except Exception as e:
            self.status_label.configure(text=f"Error: {e}")


def download_audio(video_url, output_dir):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
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
                print(f'Successfully downloaded audio file: {file_path}')
        else:
            # Single video
            file_path = ydl.prepare_filename(info_dict)
            print(f'Successfully downloaded audio file: {file_path}')
        return file_path


if __name__ == '__main__':
    root = tk.Tk()
    gui = AudioDownloaderGUI(root)
    root.mainloop()
