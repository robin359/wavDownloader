import os
import yt_dlp
import tkinter as tk
from tkinter import filedialog

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


def choose_directory():
    output_dir = filedialog.askdirectory()
    if output_dir:
        directory_entry.delete(0, tk.END)
        directory_entry.insert(0, output_dir)


def download():
    url = url_entry.get()
    output_dir = directory_entry.get()
    try:
        os.makedirs(output_dir, exist_ok=True)
        audio_file_path = download_audio(url, output_dir)
        status_label.config(text=f'Successfully downloaded audio file: {audio_file_path}')
    except Exception as e:
        status_label.config(text=f'Error: {e}')


root = tk.Tk()
root.title('YouTube Audio Downloader')

# URL Entry
url_label = tk.Label(root, text='Enter the YouTube video/playlist URL:')
url_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')

url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')

# Directory Entry
directory_label = tk.Label(root, text='Choose the directory to store the files:')
directory_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')

directory_entry = tk.Entry(root, width=50)
directory_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')

directory_button = tk.Button(root, text='Choose Directory', command=choose_directory)
directory_button.grid(row=1, column=2, padx=10, pady=10, sticky='w')

# Download Button
download_button = tk.Button(root, text='Download Audio', command=download)
download_button.grid(row=2, column=0, padx=10, pady=10)

# Status Label
status_label = tk.Label(root, text='', fg='green')
status_label.grid(row=2, column=1, padx=10, pady=10, sticky='w')

# Set minimum window size
root.minsize(600, 150)

# Center window on screen
root.eval('tk::PlaceWindow . center')

root.mainloop()
