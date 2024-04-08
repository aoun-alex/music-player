import tkinter as tk
import vlc
import radio_search_function as rsf
from radio_favorites import FavoritesManager, JSONStorageManager
from recently_played import RecentlyPlayed, StationFactory


class RadioFacade:
    def __init__(self):
        self.radio_player = RadioPlayer()

    def run(self):
        self.radio_player.run()

    def search_station(self, query):
        return self.radio_player.search_station(query)

    def search_genre(self, query):
        return self.radio_player.search_genre(query)

    def add_to_favorites(self, station_name, station_url):
        self.radio_player.add_to_favorites(station_name, station_url)

    def remove_from_favorites(self, station_name, station_url):
        self.radio_player.remove_from_favorites(station_name, station_url)

    def play_radio(self, url):
        self.radio_player.play_radio(url)


class RadioPlayer:
    def __init__(self):
        self.station_adapter = rsf.StationAdapter('stations.csv')
        self.stations, self.genres = self.station_adapter.load_stations('stations.csv')
        self.player = vlc.MediaPlayer()
        self.root = tk.Tk()
        self.root.geometry("500x500")
        self.root.title("Radio Player")
        self.storage_manager = JSONStorageManager('favorites.json')  # Create an instance of JSONStorageManager
        self.favorites_manager = FavoritesManager(
            self.storage_manager)  # Pass the storage_manager instance to FavoritesManager
        self.station_factory = StationFactory()  # Create an instance of StationFactory
        self.recently_played_manager = RecentlyPlayed(self.station_factory)  # Pass the station_factory instance to RecentlyPlayed
        self.create_main_menu()

    def create_main_menu(self):
        self.clear_window(self.root)
        tk.Button(self.root, text="Search Station", command=self.search_station, width=20, height=2).pack(pady=5)
        tk.Button(self.root, text="Search Genre", command=self.search_genre, width=20, height=2).pack(pady=5)
        tk.Button(self.root, text="Display Genre", command=self.display_genre, width=20, height=2).pack(pady=5)
        tk.Button(self.root, text="Favorite Stations", command=self.display_favorite_stations, width=20, height=2).pack(
            pady=5)
        tk.Button(self.root, text="Recently Played", command=self.display_recently_played, width=20, height=2).pack(
            pady=5)
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
        matches = self.station_adapter.search_station(query)
        if matches:
            for i, match in enumerate(matches, start=1):
                station_button = tk.Button(window, text=f"{i}. {match[0]}: {match[1]}",
                                           command=lambda s=match[0]: self.play_radio(self.stations[s]))
                station_button.pack()
                add_button = tk.Button(window, text="Add to Favorites",
                                       command=lambda s=match[0]: self.add_to_favorites(s, match[1]))
                add_button.pack()
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

        matches = self.station_adapter.search_genre(query)
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

            add_button = tk.Button(scrollable_frame, text="Add to Favorites",
                                   command=lambda s=station: self.add_to_favorites(s, self.stations[s]))
            add_button.pack(pady=3, padx=10, fill=tk.X)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        back_button = tk.Button(window, text="Back", command=go_back, width=20, height=2)
        back_button.pack(pady=10)

    def display_favorite_stations(self):
        fav_window = tk.Toplevel(self.root)
        fav_window.geometry("500x500")
        fav_window.title("Favorite Stations")
        favorites = self.favorites_manager.get_favorites()
        if favorites:
            for i, fav in enumerate(favorites, start=1):
                station_button = tk.Button(fav_window, text=f"{i}. {fav[0]}: {fav[1]}",
                                           command=lambda s=fav[0]: self.play_radio(self.stations[s]))
                station_button.pack()
                remove_button = tk.Button(fav_window, text="Remove from Favorites",
                                          command=lambda s=fav[0]: self.remove_from_favorites(s, fav[1]))
                remove_button.pack()
        else:
            tk.Label(fav_window, text="No favorite stations.").pack()

    def remove_from_favorites(self, station_name, station_url):
        self.favorites_manager.remove_from_favorites(station_name, station_url)
        self.display_favorite_stations()

    def add_to_favorites(self, station_name, station_url):
        self.favorites_manager.add_to_favorites(station_name, station_url)
        self.display_favorite_stations()

    def display_recently_played(self):
        rp_window = tk.Toplevel(self.root)
        rp_window.geometry("500x500")
        rp_window.title("Recently Played Stations")
        recently_played = self.recently_played_manager.get_recently_played()
        if recently_played:
            for i, rp in enumerate(recently_played, start=1):
                station_button = tk.Button(rp_window, text=f"{i}. {rp[0]}",
                                           command=lambda s=rp[1]: self.play_radio(s))
                station_button.pack()
        else:
            tk.Label(rp_window, text="No recently played stations.").pack()

    def get_station_info(self, url):
        # Use the URL to get the station name from the stations dictionary
        station_name = self.stations.get(url)
        if station_name is None:
            station_name = url  # Use the URL as the station name if the station name is not found
        return station_name, url

    def play_radio(self, url):
        self.player.stop()
        self.player = vlc.MediaPlayer(url)
        self.player.play()
        station_name, station_url = self.get_station_info(url)
        self.recently_played_manager.add(station_name, station_url)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    RadioFacade().run()
