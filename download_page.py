import subprocess
import os
from tkinter import Listbox, Toplevel, Label, END, messagebox, filedialog
from customtkinter import CTkButton, CTkEntry
from api import search
from abc import ABC, abstractmethod

#Abstract Factory

class AbstractFactory(ABC):
    # Abstract factory class
    @abstractmethod
    def create_downloader(self):
        pass


class AbstractDownloader(ABC):
    # Abstract downloader class
    @abstractmethod
    def download(self, url, path):
        pass


class AudioDownloader(AbstractDownloader):
    # Downloader subclass for audio files
    def download(self, url, path):
        # Download audio file
        print(f"Starting audio download for {url}...")
        subprocess.run([
            'yt-dlp',
            '-f', 'bestaudio',
            '-o', f'{path}/%(title)s.%(ext)s',
            '--extract-audio',
            '--audio-format', 'mp3',
            '--add-metadata',
            url
        ])
        print("Audio download finished!")


class VideoDownloader(AbstractDownloader):
    # Downloader subclass for video files
    def download(self, url, path):
        # Download video file
        print(f"Starting video download for {url}...")
        subprocess.run([
            'yt-dlp',
            '-f', 'bestvideo+bestaudio',
            '-o', f'{path}/%(title)s.%(ext)s',
            '--add-metadata',
            url
        ])
        print("Video download finished!")


class AudioDownloaderFactory(AbstractFactory):
    # Factory subclass for audio downloaders
    def create_downloader(self):
        return AudioDownloader()


class VideoDownloaderFactory(AbstractFactory):
    # Factory subclass for video downloaders
    def create_downloader(self):
        return VideoDownloader()


def download_song(root):
    # Function to download a song
    results = []

    def on_song_select(event):
        # Event handler for selecting a song
        widget = event.widget
        selection = widget.curselection()
        video_id = results[selection[0]]['videoId']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        download_path = filedialog.askdirectory(initialdir=get_last_used_directory())
        set_last_used_directory(download_path)
        factory = AudioDownloaderFactory()  # or VideoDownloaderFactory()
        downloader = factory.create_downloader()
        downloader.download(video_url, download_path)
        download_window.destroy()
        messagebox.showinfo("Download Complete", "The song has been downloaded successfully!")

    def submit(event=None):
        # Function to handle submission of search query
        nonlocal results
        nonlocal listbox
        query = entry.get()
        results = search(query)
        listbox.delete(0, END)
        for result in results[:5]:
            listbox.insert(END, result['title'])

    download_window = Toplevel(root)
    download_window.geometry("500x500")
    Label(download_window, text="Enter a song title: ").pack()
    entry = CTkEntry(download_window, width=200, height=25)
    entry.place(x=0, y=0)
    entry.pack()
    entry.bind('<Return>', submit)
    listbox = Listbox(download_window, width=60)
    listbox.pack()
    listbox.bind('<<ListboxSelect>>', on_song_select)
    CTkButton(download_window, text="Submit", command=submit).pack()


def get_last_used_directory():
    # Function to get the last used directory
    try:
        with open('last_used_directory.txt', 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return os.getcwd()


def set_last_used_directory(directory):
    # Function to set the last used directory
    with open('last_used_directory.txt', 'w') as file:
        file.write(directory)
