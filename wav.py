import os
import yt_dlp


def download_audio(video_url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=True)
        file_path = ydl.prepare_filename(info_dict)
        return file_path


if __name__ == '__main__':
    url = input('Enter the YouTube video URL: ')
    audio_file_path = download_audio(url)
    print(f'Successfully downloaded audio file: {audio_file_path}')
