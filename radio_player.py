import tkinter as tk
import vlc
import radio_search_function as rsf


class RadioPlayer:
    def __init__(self):
        self.stations, self.genres = rsf.load_stations('stations.csv')
        self.player = vlc.MediaPlayer()
        self.root = tk.Tk()
        self.root.geometry("500x500")
        self.root.title("Radio Player")
        self.create_main_menu()


    def create_main_menu(self):
        self.clear_window(self.root)
        tk.Button(self.root, text="Search Station", command=self.search_station, width=20, height=2).pack(pady=5)
        tk.Button(self.root, text="Search Genre", command=self.search_genre, width=20, height=2).pack(pady=5)
        tk.Button(self.root, text="Display Genre", command=self.display_genre, width=20, height=2).pack(pady=5)
        tk.Button(self.root, text="Quit", command=self.root.quit, width=20, height=2).pack(pady=5)

    def clear_window(self, window):
        for widget in window.winfo_children():
            widget.destroy()

    def search_station(self):
        search_window = tk.Toplevel(self.root)
        search_window.geometry("500x500")
        search_window.title("Search Station")
        tk.Label(search_window, text="Enter the name of the station:").pack()
        search_entry = tk.Entry(search_window)
        search_entry.pack()
        search_entry.bind('<Return>', lambda event: self.display_search_results(search_window, search_entry.get()))
        tk.Button(search_window, text="Cancel", command=search_window.destroy, width=20, height=2).pack(pady=5)

    def display_search_results(self, window, query):
        for widget in window.winfo_children():
            if isinstance(widget, tk.Label):
                widget.destroy()
        matches = rsf.search_station(self.stations, query)
        if matches:
            for i, match in enumerate(matches, start=1):
                station_button = tk.Button(window, text=f"{i}. {match[0]}: {match[1]}",
                                           command=lambda s=match[0]: self.play_radio(self.stations[s]))
                station_button.pack()
        else:
            tk.Label(window, text="No matching stations found.").pack()

    def search_genre(self):
        search_window = tk.Toplevel(self.root)
        search_window.geometry("500x500")
        search_window.title("Search Genre")

        tk.Label(search_window, text="Enter the genre:").pack()
        search_entry = tk.Entry(search_window)
        search_entry.pack()
        search_entry.bind('<Return>', lambda event: self.display_genre_results(search_window, search_entry.get()))

        cancel_button = tk.Button(search_window, text="Cancel", command=search_window.destroy, width=20, height=2)
        cancel_button.pack(pady=5)

    def display_genre_results(self, window, query):
        for widget in window.winfo_children():
            widget.destroy()

        canvas = tk.Canvas(window)
        scrollbar = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        matches = rsf.search_genre(self.genres, query)
        if matches:
            for i, match in enumerate(matches, start=1):
                genre_label = tk.Label(scrollable_frame, text=f"{i}. {match[0]}:")
                genre_label.pack()
                for station in match[1]:
                    station_button = tk.Button(scrollable_frame, text=station,
                                               command=lambda s=station: self.play_radio(self.stations[s]),
                                               width=50, height=1,  # Adjusted width to be longer
                                               bd=2, relief=tk.RAISED, bg="lightgray",
                                               # Thinner border and raised appearance
                                               wraplength=200)  # Wrap text if it exceeds 200 pixels in width
                    station_button.pack(pady=3, padx=10,
                                        fill=tk.X)  # Added padding and fill option to expand horizontally
        else:
            tk.Label(scrollable_frame, text="No matching genres found.").pack()

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def display_genre(self):
        genre_window = tk.Toplevel(self.root)
        genre_window.geometry("500x500")
        genre_window.title("Display Genre")

        canvas = tk.Canvas(genre_window)
        scrollbar = tk.Scrollbar(genre_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        for genre in self.genres:
            genre_button = tk.Button(
                scrollable_frame, text=genre,
                command=lambda g=genre: self.display_stations(genre_window, g),
                width=30, height=1,
                bd=2, relief=tk.RAISED, bg="lightgray"
            )
            genre_button.pack(pady=3, padx=10, fill=tk.X)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        cancel_button = tk.Button(genre_window, text="Cancel", command=genre_window.destroy, width=20, height=2)
        cancel_button.pack(pady=10)

        genre_window.mainloop()

    def display_stations(self, window, genre):
        def go_back():
            window.destroy()
            self.display_genre()

        self.clear_window(window)

        canvas = tk.Canvas(window)
        scrollbar = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        stations = self.genres[genre]
        for station in stations:
            station_button = tk.Button(
                scrollable_frame, text=station,
                command=lambda s=station: self.play_radio(self.stations[s]),
                width=50, height=1,  # Adjusted width to be longer
                bd=2, relief=tk.RAISED, bg="lightgray",  # Thinner border and raised appearance
                wraplength=200  # Wrap text if it exceeds 200 pixels in width
            )
            station_button.pack(pady=3, padx=10, fill=tk.X)  # Added padding and fill option to expand horizontally

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        back_button = tk.Button(window, text="Back", command=go_back, width=20, height=2)
        back_button.pack(pady=10)

    def play_radio(self, url):
        self.player.stop()
        self.player = vlc.MediaPlayer(url)
        self.player.play()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    RadioPlayer().run()
