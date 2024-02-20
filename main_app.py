from customtkinter import CTkButton, CTkEntry
from tkinter import Tk, Toplevel, Label, END, messagebox, Listbox
from song_menu import create_gui, get_songs
from api import search
import subprocess
from abc import ABC, abstractmethod


# Function to download audio from YouTube using yt-dlp
def download_audio(url, path):
    print(f"Starting download for {url}...")
    subprocess.run([
        'yt-dlp',
        '-f', 'bestaudio',
        '-o', f'{path}/%(title)s.%(ext)s',
        '--extract-audio',
        '--audio-format', 'mp3',
        '--add-metadata',
        url
    ])


# Abstract class for observers
class Observer(ABC):
    @abstractmethod
    def update(self, *args, **kwargs):
        pass


# Observable class for implementing observer pattern
class Observable: #TODO notify the user when a song is downloaded
    def __init__(self):
        self._observers = []

    def subscribe(self, observer):
        self._observers.append(observer)

    def unsubscribe(self, observer):
        self._observers.remove(observer)

    def notify(self, *args, **kwargs):
        for observer in self._observers:
            observer.update(*args, **kwargs)


# Abstract class for button commands
class ButtonCommand(ABC):
    @abstractmethod
    def execute(self):
        pass


class DownloadSongCommand(ButtonCommand):
    def execute(self):
        download_song()


class PlaySongCommand(ButtonCommand):
    def execute(self):
        play_song()


class ExitCommand(ButtonCommand):
    def execute(self):
        root.quit()


# Factory class for creating button commands
class ButtonFactory:
    @staticmethod
    def create_button(type):
        if type == "Download":
            return DownloadSongCommand()
        elif type == "Play":
            return PlaySongCommand()
        elif type == "Exit":
            return ExitCommand()
        else:
            raise ValueError("Invalid button type")


# Decorator function to print start and end of download
def download_decorator(func): #TODO: remove this soon
    def wrapper(*args, **kwargs):
        print("Starting download...")
        result = func(*args, **kwargs)
        print("Download finished!")
        return result

    return wrapper


# Function to download a song
@download_decorator
def download_song():
    # Initialize variables and GUI elements
    results = []
    listbox = Listbox()

    # Function to handle song selection from listbox
    def on_song_select(event):
        print("Song selected...")
        nonlocal results
        widget = event.widget
        selection = widget.curselection()
        video_id = results[selection[0]]['videoId']
        print(f"Selected video ID: {video_id}")
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        print(f"Video URL: {video_url}")
        download_path = r"C:\Users\alexa\Documents\GitHub\music-player\music"
        print(f"Download path: {download_path}")
        download_audio(video_url, download_path)
        download_window.destroy()
        messagebox.showinfo("Download Complete", "The song has been downloaded successfully!")

    # Function to submit search query and display results
    def submit(event=None):
        nonlocal results
        nonlocal listbox
        query = entry.get()
        results = search(query)
        listbox.delete(0, END)
        for result in results[:5]:
            listbox.insert(END, result['title'])

    # Creating GUI for downloading a song
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


# Function to play a downloaded song
def play_song():  # TODO: implement flexible directory instead of hardcoded
    directory = r"C:\Users\alexa\Documents\GitHub\music-player\music"
    songs = get_songs(directory)
    create_gui(songs, directory)


# Main GUI class that acts as an observer
class MainGui(Observer):
    def update(self, *args, **kwargs):
        pass

    # Function to create the main GUI
    def create_main_gui(self):
        global root
        root = Tk()
        root.geometry("500x500")
        CTkButton(root, text="Download new song from YouTube",
                  command=ButtonFactory.create_button("Download").execute).pack()
        CTkButton(root, text="Play a downloaded song", command=ButtonFactory.create_button("Play").execute).pack()
        CTkButton(root, text="Exit", command=ButtonFactory.create_button("Exit").execute).pack()
        root.mainloop()


# Main function to run the application
def main():
    main_gui = MainGui()
    download_song = Observable()
    download_song.subscribe(main_gui)
    main_gui.create_main_gui()


# Entry point of the program
if __name__ == "__main__":
    main()
