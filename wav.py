import os
import yt_dlp


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
    while True:
        url = input('Enter the YouTube video/playlist URL: ')
        output_dir = input('Enter the directory to store the files: ')
        try:
            os.makedirs(output_dir, exist_ok=True)
            audio_file_path = download_audio(url, output_dir)
            print(f'Successfully downloaded audio file: {audio_file_path}')
        except Exception as e:
            print(f'Error: {e}')

        choice = input('Do you want to download another video/playlist? [y/n]: ')
        if choice.lower() != 'y':
            break
