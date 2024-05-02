import tkinter as tk
from radio_player import RadioFacade
from youtube_importer import GuiBuilder

class MainApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("500x500")
        self.root.title("Music App")
        tk.Label(self.root, text="Please pick an option:", font=("Helvetica", 14)).pack()

        tk.Button(self.root, text="YouTube Importer", command=self.open_youtube_importer).pack()
        tk.Button(self.root, text="Radio Player", command=self.open_radio_player).pack()
        tk.Button(self.root, text="Quit", command=self.root.quit).pack()

    def open_youtube_importer(self):
        GuiBuilder().create_main_window().add_download_button().add_play_button().add_exit_button().start_main_loop()

    def open_radio_player(self):
        RadioFacade().run()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    MainApp().run()