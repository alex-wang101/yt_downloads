import yt_dlp
import os
import re

def download_video(url, download_type):
    global generated_files
    ydl_opts = {
        'outtmpl': '%(title)s.%(ext)s',
        'noplaylist': True,
    }

    if download_type == 'video' or download_type == 'both':
        ydl_opts['format'] = 'bestvideo[height<=1080]+bestaudio/best'
        ydl_opts['merge_output_format'] = 'mp4'

    if download_type == 'transcript' or download_type == 'both':
        ydl_opts['writesubtitles'] = True
        ydl_opts['subtitlesformat'] = 'vtt'
        ydl_opts['subtitleslangs'] = ['en']
        ydl_opts['writeautomaticsub'] = True

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        video_title = info_dict.get('title', 'video')

        # Downloads as mp4
        if download_type == 'video' or download_type == 'both':
            video_file = f"{video_title}.mp4"
            generated_files.append(video_file)

        # Saves subtitles as .vtt file
        if download_type == 'transcript' or download_type == 'both':
            subtitle_file = f"{video_title}.en.vtt"
            if os.path.exists(subtitle_file):
                with open(subtitle_file, 'r', encoding='utf-8') as file:
                    subtitle_content = file.read()

                # Clean up the subtitle content
                cleaned_transcript = clean_subtitles(subtitle_content)

                # Save the cleaned transcript
                transcript_file = f"{video_title}_transcript.txt"
                with open(transcript_file, 'w', encoding='utf-8') as file:
                    file.write(cleaned_transcript)
                print(f"Cleaned transcript saved as {transcript_file}")

                generated_files.append(subtitle_file)
                generated_files.append(transcript_file)
            else:
                print("No subtitles found for this video.")

def clean_subtitles(subtitle_content):
    cleaned_lines = []
    for line in subtitle_content.splitlines():
        if not line.strip() or line.startswith(('WEBVTT', 'Kind:', 'Language:')):
            continue
        if re.match(r'\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}', line):
            continue
        if re.match(r'align:\w+ position:\d+%', line):
            continue
        line = re.sub(r'<[^>]+>', '', line)
        cleaned_lines.append(line.strip())

    #Cleans transcript to make it readable 
    cleaned_transcript = ' '.join(cleaned_lines)
    cleaned_transcript = re.sub(r'\s+', ' ', cleaned_transcript).strip()
    return cleaned_transcript

if __name__ == "__main__":
    generated_files = []
    while True:
        video_url = input("Enter URL: ").strip()

        print("Choose what to download:")
        print("1. Video only")
        print("2. Transcript only")
        print("3. Both video and transcript")
        choice = input("Enter your choice (1/2/3): ").strip()

        if choice == '1':
            download_type = 'video'
        elif choice == '2':
            download_type = 'transcript'
        elif choice == '3':
            download_type = 'both'
        else:
            print("Invalid choice. Please try again.")
            continue

        download_video(video_url, download_type)