import yt_dlp

def download_video(url):
    ydl_opts = {
        'format': 'bestvideo[height<=1080]+bestaudio/best',  # selects the best video and audio within the resolution limit
        'outtmpl': '%(title)s.%(ext)s',  # sets the output filename to the video title
        'merge_output_format': 'mp4',  # ensures the final file is in MP4 format
        'noplaylist': True,  # avoids downloading entire playlists
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    video_url = input("Enter URL: ")
    download_video(video_url)