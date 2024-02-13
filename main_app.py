from api import search
import subprocess
import vlc


def download_audio(url, path):
    subprocess.run([
        'yt-dlp',
        '-f', 'bestaudio',
        '-o', f'{path}/%(title)s.%(ext)s',
        '--extract-audio',
        '--audio-format', 'mp3',
        '--add-metadata',
        url
    ])


def play_audio(path):
    player = vlc.MediaPlayer(path)
    player.play()


def main():
    while True:
        print("1. Download new song from YouTube")
        print("2. Play a downloaded song")
        print("3. Exit")
        choice = int(input("Select an option (1-3): "))

        if choice == 1:
            query = input("Enter a song title: ")
            results = search(query)

            for i, result in enumerate(results, start=1):
                print(f"{i}. {result['title']}")

            song_choice = int(input("Select a song (1-5): ")) - 1
            video_id = results[song_choice]['videoId']
            video_url = f"https://www.youtube.com/watch?v={video_id}"

            print("Downloading audio...")
            download_path = r"C:\Users\alexa\Documents\GitHub\music-player\music"
            download_audio(video_url, download_path)

        elif choice == 2:
            audio_path = input("Enter the path of the mp3: ")
            print("Playing audio...")
            play_audio(audio_path)

        elif choice == 3:
            print("Exiting program...")
            break

        else:
            print("Invalid option. Please select 1, 2 or 3.")


if __name__ == "__main__":
    main()
