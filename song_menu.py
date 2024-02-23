import os
import vlc
from tkinter import Tk, Listbox, Button, END


def get_songs(directory):
    songs = [file for file in os.listdir(directory) if file.endswith(".mp3")]
    return songs


class SongPlayer:
    def __init__(self):
        self.player = None

    def play_song(self, song_path):
        if self.player:
            self.player.stop()
        self.player = vlc.MediaPlayer(song_path)
        self.player.play()

    def pause_song(self):
        if self.player:
            self.player.pause()

    def resume_song(self):
        if self.player:
            self.player.play()

    def stop_song(self):
        if self.player:
            self.player.stop()


song_player = SongPlayer()


def on_song_select(event, directory):
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
        song_player.play_song(song_path)


def create_gui(songs, directory):
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
