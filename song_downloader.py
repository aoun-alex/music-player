import os
import subprocess
import shutil
import json
import tkinter as tk
from tkinter import messagebox, filedialog


# Template Method

def load_credentials():
    with open('secret.json', 'r') as f:
        credentials = json.load(f)
    return credentials


credentials = load_credentials()
os.environ['SPOTIPY_CLIENT_ID'] = credentials['spotify_client_id']
os.environ['SPOTIPY_CLIENT_SECRET'] = credentials['spotify_client_secret']


class SpotifyDownloader:
    def __init__(self, spotify_url):
        self.spotify_url = spotify_url
        self.output_dir = None

    # The template method that defines the skeleton of the operation.
    def download_spotify_content(self):
        self.setup_output_directory()
        self.run_command()
        self.move_files()
        self.cleanup()
        self.notify_user()

    # Set up or confirm the output directory for downloads.
    def setup_output_directory(self):
        # Use a file dialog to allow the user to choose a directory if not set.
        if self.output_dir is None:
            root = tk.Tk()
            root.withdraw()
            self.output_dir = filedialog.askdirectory()

            # Save the chosen directory to a JSON file for future use.
            if self.output_dir:
                with open('download_directory.json', 'w') as f:
                    json.dump({'download_directory': self.output_dir}, f)
            else:
                return

        else:
            # Load and possibly update the saved directory.
            try:
                with open('download_directory.json', 'r') as f:
                    saved_dir = json.load(f)['download_directory']
                if saved_dir != self.output_dir:
                    with open('download_directory.json', 'w') as f:
                        json.dump({'download_directory': self.output_dir}, f)
            except FileNotFoundError:
                with open('download_directory.json', 'w') as f:
                    json.dump({'download_directory': self.output_dir}, f)

    # Execute the command to download content.
    def run_command(self):
        command = ['spotify_dl', '-l', self.spotify_url, '-o', self.output_dir]
        subprocess.run(command)

    # Move downloaded files from nested folders to the main directory.
    def move_files(self):
        for root, dirs, files in os.walk(self.output_dir):
            for file in files:
                if file.endswith('.mp3'):
                    source = os.path.join(root, file)
                    destination = os.path.join(self.output_dir, file)
                    shutil.move(source, destination)

    # Clean up empty directories left after moving files.
    def cleanup(self):
        for root, dirs, files in os.walk(self.output_dir, topdown=False):
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                if not os.listdir(dir_path):
                    os.rmdir(dir_path)

    def notify_user(self):
        messagebox.showinfo("Download Complete", "Your content has been downloaded successfully.")


# Main function to run the GUI application.
def main():
    root = tk.Tk()
    root.geometry("500x500")
    root.title("Spotify Track Downloader")

    # Function to trigger the download process.
    def trigger_download():
        spotify_url = url_entry.get()
        try:
            with open('download_directory.json', 'r') as f:
                output_dir = json.load(f)['download_directory']
        except (FileNotFoundError, KeyError):
            output_dir = None

        downloader = SpotifyDownloader(spotify_url)
        downloader.download_spotify_content()

    url_label = tk.Label(root, text="Enter Spotify track/playlist URL:")
    url_label.pack(pady=20)

    url_entry = tk.Entry(root, width=40)
    url_entry.pack()

    download_btn = tk.Button(root, text="Download", command=trigger_download)
    download_btn.pack(pady=20)

    root.mainloop()


if __name__ == "__main__":
    main()
