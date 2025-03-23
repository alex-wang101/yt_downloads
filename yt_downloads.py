import yt_dlp

def download_video(url):
    ydl_opts = {
        'format': 'bestvideo[height<=1080]+bestaudio/best',  
        'outtmpl': '%(title)s.%(ext)s',  
        'merge_output_format': 'mp4',  
        'noplaylist': True,
        'postprocessors': [{  
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',  
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    video_url = input("Enter URL: ")
    download_video(video_url)