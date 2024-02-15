import os
import vlc
from tkinter import Tk, Listbox, Button, END
from abc import ABC, abstractmethod

player = None


def get_songs(directory):
    songs = []
    for file in os.listdir(directory):
        if file.endswith(".mp3"):
            songs.append(file)
    return songs


class ButtonCommand(ABC):
    @abstractmethod
    def execute(self):
        pass


class PlaySongCommand(ButtonCommand):
    def __init__(self, song_path):
        self.song_path = song_path

    def execute(self):
        global player
        player = vlc.MediaPlayer(self.song_path)
        player.play()


class PauseSongCommand(ButtonCommand):
    def execute(self):
        global player
        if player:
            player.pause()


class ResumeSongCommand(ButtonCommand):
    def execute(self):
        global player
        if player:
            player.play()


class StopSongCommand(ButtonCommand):
    def execute(self):
        global player
        if player:
            player.stop()


class ButtonFactory:
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
        else:
            raise ValueError("Invalid button type")


def song_decorator(func):
    def wrapper(*args, **kwargs):
        print("Starting song operation...")
        result = func(*args, **kwargs)
        print("Song operation finished!")
        return result

    return wrapper


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


def on_song_select(event, directory):
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
