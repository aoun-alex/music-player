import tkinter as tk
from tkinter import filedialog
from song_menu import create_gui, get_songs
from download_page import download_song, get_last_used_directory, set_last_used_directory


class MainGui:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("500x500")

    def create_main_gui(self):
        tk.Button(self.root, text="Download new song from YouTube", command=self.download_song).pack()
        tk.Button(self.root, text="Play a downloaded song", command=self.play_song).pack()
        tk.Button(self.root, text="Exit", command=self.exit_app).pack()
        self.root.mainloop()

    def download_song(self):
        directory = filedialog.askdirectory(initialdir=get_last_used_directory())
        set_last_used_directory(directory)
        download_song(self.root)

    def play_song(self):
        directory = filedialog.askdirectory(initialdir=get_last_used_directory())
        set_last_used_directory(directory)
        songs = get_songs(directory)
        create_gui(songs, directory)

    def exit_app(self):
        self.root.quit()


def main():
    main_gui = MainGui()
    main_gui.create_main_gui()


if __name__ == "__main__":
    main()
