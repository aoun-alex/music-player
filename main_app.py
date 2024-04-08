import tkinter as tk
from tkinter import filedialog
from song_menu import create_gui, get_songs
from download_page import download_song, get_last_used_directory, set_last_used_directory


class GuiBuilder:
    def __init__(self):
        self.gui = MainGui()

    def create_main_window(self):
        self.gui.root = tk.Tk()
        self.gui.root.geometry("500x500")
        return self

    def add_download_button(self):
        tk.Button(self.gui.root, text="Download new song from YouTube", command=self.gui.download_song).pack()
        return self

    def add_play_button(self):
        tk.Button(self.gui.root, text="Play a downloaded song", command=self.gui.play_song).pack()
        return self

    def add_exit_button(self):
        tk.Button(self.gui.root, text="Exit", command=self.gui.exit_app).pack()
        return self

    def start_main_loop(self):
        self.gui.root.mainloop()
        return self

    def get_result(self):
        return self.gui


class MainGui:
    def __init__(self):
        self.root = None

    def download_song(self):
        # Function to handle downloading a song
        directory = filedialog.askdirectory(initialdir=get_last_used_directory())
        set_last_used_directory(directory)
        download_song(self.root)

    def play_song(self):
        # Function to handle playing a song
        directory = filedialog.askdirectory(initialdir=get_last_used_directory())
        set_last_used_directory(directory)
        songs = get_songs(directory)
        create_gui(songs, directory)

    def exit_app(self):
        self.root.quit()


def main():
    builder = GuiBuilder()  # Create an instance of the GuiBuilder class
    main_gui = (builder.create_main_window()
                .add_download_button()
                .add_play_button()
                .add_exit_button()
                .start_main_loop()
                .get_result())


if __name__ == "__main__":
    main()
