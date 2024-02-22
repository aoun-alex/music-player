from customtkinter import CTkButton
from tkinter import Tk, filedialog
from song_menu import create_gui, get_songs
from download_page import download_song, get_last_used_directory, set_last_used_directory
from abc import ABC, abstractmethod


# TODO: add queue and skip feature
# TODO: add live radio feature for Lab2
# TODO: better GUI
# TODO: something else I forgot
# Abstract class for observers
class Observer(ABC):
    @abstractmethod
    def update(self, *args, **kwargs):
        pass


# Observable class for implementing observer pattern
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


# Abstract class for button commands
class ButtonCommand(ABC):
    @abstractmethod
    def execute(self):
        pass


class PlaySongCommand(ButtonCommand):
    def execute(self):
        play_song()


class ExitCommand(ButtonCommand):
    def __init__(self, root):
        self.root = root

    def execute(self):
        self.root.quit()


class ButtonFactory:
    @staticmethod
    def create_button(type, root=None):
        if type == "Download":
            return DownloadSongCommand(root)
        elif type == "Play":
            return PlaySongCommand()
        elif type == "Exit":
            return ExitCommand(root)
        else:
            raise ValueError("Invalid button type")


# Function to play a downloaded song
def play_song():
    directory = filedialog.askdirectory(initialdir=get_last_used_directory())
    set_last_used_directory(directory)
    songs = get_songs(directory)
    create_gui(songs, directory)


# Main GUI class that acts as an observer
class MainGui(Observer):
    def __init__(self):
        self.root = Tk()
        self.root.geometry("500x500")

    def update(self, *args, **kwargs):
        pass

    # Function to create the main GUI
    def create_main_gui(self):
        CTkButton(self.root, text="Download new song from YouTube",
                  command=ButtonFactory.create_button("Download", self.root).execute).pack()
        CTkButton(self.root, text="Play a downloaded song", command=ButtonFactory.create_button("Play").execute).pack()
        CTkButton(self.root, text="Exit", command=ButtonFactory.create_button("Exit", self.root).execute).pack()
        self.root.mainloop()


class DownloadSongCommand(ButtonCommand):
    def __init__(self, root):
        self.root = root

    def execute(self):
        download_song(self.root)


# Main function to run the application
def main():
    main_gui = MainGui()
    download_song = Observable()
    download_song.subscribe(main_gui)
    main_gui.create_main_gui()


# Entry point of the program
if __name__ == "__main__":
    main()
