import os
import vlc
from tkinter import Tk, Listbox, Button, END

#Prototype

def get_songs(directory):
    # Get a list of songs in the specified directory.
    songs = [file for file in os.listdir(directory) if file.endswith(".mp3")]
    return songs


class SongPlayer:
    # Class to handle playing, pausing, resuming, and stopping songs.

    def __init__(self):
        self.player = None

    def play_song(self, song_path):
        # Play the specified song.
        if self.player:
            self.player.stop()
        self.player = vlc.MediaPlayer(song_path)
        self.player.play()

    def pause_song(self):
        # Pause the currently playing song.
        if self.player:
            self.player.pause()

    def resume_song(self):
        # Resume the paused song.
        if self.player:
            self.player.play()

    def stop_song(self):
        # Stop the currently playing song.
        if self.player:
            self.player.stop()


class SongPrototype:
    # Prototype class for cloning SongPlayer instances.

    def __init__(self, song_player):
        self.song_player = song_player

    def clone(self):
        # Clone the SongPlayer instance.
        new_song_player = SongPlayer()
        new_song_player.player = self.song_player.player
        return new_song_player


song_player = SongPlayer()


def on_song_select(event, directory):
    # Event handler for selecting a song from the list.
    global song_player
    widget = event.widget
    selection = widget.curselection()
    song = widget.get(selection[0])
    song_path = os.path.join(directory, song)
    if song_player.player and song_player.player.get_media().get_mrl() == song_path:
        if song_player.player.is_playing():
            song_player.pause_song()
        else:
            song_player.resume_song()
    else:
        song_player.stop_song()
        new_song_player = SongPrototype(song_player).clone()
        song_player.player = new_song_player.player
        song_player.play_song(song_path)


def create_gui(songs, directory):
    # Create the GUI for playing songs.
    root = Tk()
    root.geometry("400x500")
    listbox = Listbox(root, width=60)
    listbox.bind('<<ListboxSelect>>', lambda event: on_song_select(event, directory))

    for song in songs:
        listbox.insert(END, song)

    pause_button = Button(root, text="Pause", command=song_player.pause_song)
    resume_button = Button(root, text="Resume", command=song_player.resume_song)

    listbox.pack()
    pause_button.pack()
    resume_button.pack()

    root.mainloop()
