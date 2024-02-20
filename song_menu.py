import os
import vlc
from tkinter import Tk, Listbox, Button, END
from abc import ABC, abstractmethod

player = None  # Variable to hold the VLC media player instance


def get_songs(directory):
    # Function to get a list of .mp3 files in a given directory.
    songs = []
    for file in os.listdir(directory):
        if file.endswith(".mp3"):
            songs.append(file)
    return songs


class ButtonCommand(ABC):
    # Abstract base class for button command objects.
    @abstractmethod
    def execute(self):
        pass


class PlaySongCommand(ButtonCommand):
    # Concrete command class for playing a song.
    def __init__(self, song_path):
        self.song_path = song_path

    def execute(self):
        global player
        player = vlc.MediaPlayer(self.song_path)
        player.play()


class PauseSongCommand(ButtonCommand):
    # Concrete command class for pausing the currently playing song.
    def execute(self):
        global player
        if player:
            player.pause()


class ResumeSongCommand(ButtonCommand):
    # Concrete command class for resuming the currently paused song.
    def execute(self):
        global player
        if player:
            player.play()


class StopSongCommand(ButtonCommand):
    # Concrete command class for stopping the currently playing song.
    def execute(self):
        global player
        if player:
            player.stop()


class ButtonFactory:
    # Factory class to create button command objects.
    @staticmethod
    def create_button(type, song_path=None):
        if type == "Play":
            return PlaySongCommand(song_path)
        elif type == "Pause":
            return PauseSongCommand()
        elif type == "Resume":
            return ResumeSongCommand()
        elif type == "Stop":
            return StopSongCommand()



class Observer(ABC):
    # Abstract base class for observer objects.
    @abstractmethod
    def update(self, *args, **kwargs):
        pass


class Observable:
    # Observable class to manage observers and notifications.
    def __init__(self):
        self._observers = []

    def subscribe(self, observer):
        self._observers.append(observer)

    def unsubscribe(self, observer):
        self._observers.remove(observer)

    def notify(self, *args, **kwargs):
        for observer in self._observers:
            observer.update(*args, **kwargs)


def on_song_select(event, directory):
    # Callback function for song selection event.
    global player
    widget = event.widget
    selection = widget.curselection()
    song = widget.get(selection[0])
    song_path = os.path.join(directory, song)
    if player and player.get_media().get_mrl() == song_path:
        if player.is_playing():
            ButtonFactory.create_button("Pause").execute()
        else:
            ButtonFactory.create_button("Resume").execute()
    else:
        ButtonFactory.create_button("Stop").execute()
        ButtonFactory.create_button("Play", song_path).execute()


def create_gui(songs, directory):
    # Function to create the GUI.
    root = Tk()
    root.geometry("400x500")
    listbox = Listbox(root, width=60)
    listbox.bind('<<ListboxSelect>>', lambda event: on_song_select(event, directory))

    for song in songs:
        listbox.insert(END, song)

    pause_button = Button(root, text="Pause", command=ButtonFactory.create_button("Pause").execute)
    resume_button = Button(root, text="Resume", command=ButtonFactory.create_button("Resume").execute)

    listbox.pack()
    pause_button.pack()
    resume_button.pack()

    root.mainloop()
