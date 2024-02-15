from tkinter import Tk, Button, Toplevel, Label, Entry, Listbox, END, messagebox
from song_menu import create_gui, get_songs
from api import search
import subprocess
from abc import ABC, abstractmethod


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


class Observer(ABC):
    @abstractmethod
    def update(self, *args, **kwargs):
        pass


class Observable:
    def __init__(self):
        self._observers = []

    def subscribe(self, observer):
        self._observers.append(observer)

    def unsubscribe(self, observer):
        self._observers.remove(observer)

    def notify(self, *args, **kwargs):
        for observer in self._observers:
            observer.update(*args, **kwargs)


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


def download_decorator(func):
    def wrapper(*args, **kwargs):
        print("Starting download...")
        result = func(*args, **kwargs)
        print("Download finished!")
        return result

    return wrapper


@download_decorator
def download_song():
    results = []  # Define results here
    listbox = Listbox()  # Define listbox here

    def on_song_select(event):
        nonlocal results
        widget = event.widget
        selection = widget.curselection()
        video_id = results[selection[0]]['videoId']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        download_path = r"C:\Users\alexa\Documents\GitHub\music-player\music"
        download_audio(video_url, download_path)
        download_window.destroy()
        messagebox.showinfo("Download Complete", "The song has been downloaded successfully!")

    def submit(event=None):  # event parameter added
        nonlocal results
        nonlocal listbox  # Make listbox nonlocal
        query = entry.get()
        results = search(query)
        listbox.delete(0, END)  # clear the listbox
        for result in results[:5]:
            listbox.insert(END, result['title'])

    download_window = Toplevel(root)
    download_window.geometry("500x500")
    Label(download_window, text="Enter a song title: ").pack()
    entry = Entry(download_window, width=60)
    entry.pack()
    entry.bind('<Return>', submit)  # bind Enter key to submit function
    listbox = Listbox(download_window, width=60)  # Initialize listbox with download_window as parent
    listbox.pack()
    Button(download_window, text="Submit", command=submit).pack()


def play_song():
    directory = r"C:\Users\alexa\Documents\GitHub\music-player\music"
    songs = get_songs(directory)
    create_gui(songs, directory)


class MainGui(Observer):
    def update(self, *args, **kwargs):
        pass  # Update song list when a song finishes downloading

    def create_main_gui(self):
        global root
        root = Tk()
        root.geometry("500x500")
        Button(root, text="Download new song from YouTube",
               command=ButtonFactory.create_button("Download").execute).pack()
        Button(root, text="Play a downloaded song", command=ButtonFactory.create_button("Play").execute).pack()
        Button(root, text="Exit", command=ButtonFactory.create_button("Exit").execute).pack()
        root.mainloop()


def main():
    main_gui = MainGui()
    download_song = Observable()
    download_song.subscribe(main_gui)
    main_gui.create_main_gui()


if __name__ == "__main__":
    main()
