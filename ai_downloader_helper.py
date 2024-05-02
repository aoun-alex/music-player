import os
import subprocess
import shutil
import json
import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox as messagebox
from abc import ABC, abstractmethod


# Command

def load_credentials():
    with open('secret.json', 'r') as f:
        credentials = json.load(f)
    return credentials


credentials = load_credentials()
os.environ['SPOTIPY_CLIENT_ID'] = credentials['spotify_client_id']
os.environ['SPOTIPY_CLIENT_SECRET'] = credentials['spotify_client_secret']


# Abstract base class for command pattern.
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass


# Concrete command for downloading tracks.
class DownloadTrackCommand(Command):
    def __init__(self, track_url, output_dir=None, format='mp3'):
        self.track_url = track_url
        self.output_dir = output_dir
        self.format = format

    def execute(self):
        # If no output directory provided, prompt the user to select one.
        if self.output_dir is None:
            root = tk.Tk()
            root.withdraw()
            self.output_dir = filedialog.askdirectory()

            if self.output_dir:
                # Save the selected directory to a JSON file.
                with open('download_directory.json', 'w') as f:
                    json.dump({'download_directory': self.output_dir}, f)
            else:
                return  # Exit if no directory selected.

        else:
            # Check if a previously saved directory exists and update if necessary.
            try:
                with open('download_directory.json', 'r') as f:
                    saved_dir = json.load(f)['download_directory']
                    if saved_dir != self.output_dir:
                        with open('download_directory.json', 'w') as f:
                            json.dump({'download_directory': self.output_dir}, f)
            except FileNotFoundError:
                with open('download_directory.json', 'w') as f:
                    json.dump({'download_directory': self.output_dir}, f)

        # Run the command to download the track.
        command = ['spotify_dl', '-l', self.track_url, '-o', self.output_dir]
        subprocess.run(command)

        # Move downloaded files to the specified directory and clean up.
        for root, dirs, files in os.walk(self.output_dir):
            for file in files:
                if file.endswith('.mp3'):
                    source = os.path.join(root, file)
                    destination = os.path.join(self.output_dir, file)
                    shutil.move(source, destination)

        # Remove any empty directories left after moving the files.
        for root, dirs, files in os.walk(self.output_dir, topdown=False):
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                if not os.listdir(dir_path):
                    os.rmdir(dir_path)

        messagebox.showinfo("Download Complete", "Your song has been downloaded successfully.")
