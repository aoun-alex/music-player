import tkinter as tk
import subprocess


# State

# Define a base State class for managing different application states.
class State:
    def handle(self):
        pass


# State for handling AI recommendations, launches an external Python script.
class AIRecommenderState(State):
    def handle(self):
        return subprocess.Popen(["python", "ai_recommender.py"])


# State for downloading songs, launches an external Python script.
class SongDownloaderState(State):
    def handle(self):
        return subprocess.Popen(["python", "song_downloader.py"])


# State for exiting the application, terminates all running subprocesses.
class ExitState(State):
    def handle(self, main_menu):
        for process in main_menu.processes:
            process.terminate()
        main_menu.root.quit()


# Main menu class for the application, manages the GUI and states.
class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Menu")
        self.processes = []
        self.state = None

        self.ai_recommender_button = tk.Button(self.root, text="AI Recommender", command=self.open_ai_recommender)
        self.ai_recommender_button.pack()

        # Button to activate the song downloader.
        self.song_downloader_button = tk.Button(self.root, text="Song Downloader", command=self.open_song_downloader)
        self.song_downloader_button.pack()

        self.exit_button = tk.Button(self.root, text="Exit", command=self.exit_all)
        self.exit_button.pack()

    def set_state(self, state):
        self.state = state

    def on_button_click(self):
        process = self.state.handle()
        if process:
            self.processes.append(process)

    def open_ai_recommender(self):
        self.set_state(AIRecommenderState())
        self.on_button_click()

    def open_song_downloader(self):
        self.set_state(SongDownloaderState())
        self.on_button_click()

    def exit_all(self):
        self.set_state(ExitState())
        self.state.handle(self)


# Main tkinter setup.
root = tk.Tk()
root.geometry("500x500")
app = MainMenu(root)
root.mainloop()
