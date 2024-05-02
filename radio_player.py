import tkinter as tk
import vlc
import radio_search_function as rsf
from radio_favorites import FavoritesManager, JSONStorageProxy
from recently_played import RecentlyPlayed, StationFactory

#Facade

class RadioFacade:
    def __init__(self):
        self.radio_player = RadioPlayer()  # Creating an instance of the RadioPlayer class

    def run(self):
        self.radio_player.run()  # Running the radio player application

    def search_station(self, query):
        return self.radio_player.search_station(query)  # Calling the search_station method in RadioPlayer

    def search_genre(self, query):
        return self.radio_player.search_genre(query)  # Calling the search_genre method in RadioPlayer

    def add_to_favorites(self, station_name, station_url):
        self.radio_player.add_to_favorites(station_name, station_url)  # Calling the add_to_favorites method in RadioPlayer

    def remove_from_favorites(self, station_name, station_url):
        self.radio_player.remove_from_favorites(station_name, station_url)  # Calling the remove_from_favorites method in RadioPlayer

    def play_radio(self, url):
        self.radio_player.play_radio(url)  # Calling the play_radio method in RadioPlayer


class RadioPlayer:
    def __init__(self):
        self.station_adapter = rsf.StationAdapter('stations.csv')  # Creating an instance of StationAdapter with 'stations.csv'
        self.stations, self.genres = self.station_adapter.load_stations('stations.csv')  # Loading stations and genres from CSV
        self.player = vlc.MediaPlayer()  # Creating an instance of MediaPlayer from vlc module
        self.root = tk.Tk()  # Creating the main Tkinter window
        self.root.geometry("500x500")
        self.root.title("Radio Player")
        self.storage_manager = JSONStorageProxy('favorites.json')  # Creating an instance of JSONStorageManager for favorites
        self.favorites_manager = FavoritesManager(self.storage_manager)  # Creating FavoritesManager instance
        self.station_factory = StationFactory()  # Creating an instance of StationFactory
        self.recently_played_manager = RecentlyPlayed(self.station_factory)  # Creating RecentlyPlayed instance
        self.create_main_menu()

    def create_main_menu(self):
        # Method to create the main menu GUI
        self.clear_window(self.root)
        tk.Button(self.root, text="Search Station", command=self.search_station, width=20, height=2).pack(pady=5)
        tk.Button(self.root, text="Search Genre", command=self.search_genre, width=20, height=2).pack(pady=5)
        tk.Button(self.root, text="Display Genre", command=self.display_genre, width=20, height=2).pack(pady=5)
        tk.Button(self.root, text="Favorite Stations", command=self.display_favorite_stations, width=20, height=2).pack(pady=5)
        tk.Button(self.root, text="Recently Played", command=self.display_recently_played, width=20, height=2).pack(pady=5)
        tk.Button(self.root, text="Quit", command=self.root.quit, width=20, height=2).pack(pady=5)

    def clear_window(self, window):
        # Method to clear all elements from a given window
        for widget in window.winfo_children():
            widget.destroy()

    def search_station(self):
        # Method to handle station search functionality
        search_window = tk.Toplevel(self.root)
        search_window.geometry("500x500")
        search_window.title("Search Station")
        tk.Label(search_window, text="Enter the name of the station:").pack()
        search_entry = tk.Entry(search_window)
        search_entry.pack()
        # Binding Enter key to trigger search
        search_entry.bind('<Return>', lambda event: self.display_search_results(search_window, search_entry.get()))
        tk.Button(search_window, text="Cancel", command=search_window.destroy, width=20, height=2).pack(pady=5)

    def display_search_results(self, window, query):
        # Method to display search results in a given window
        for widget in window.winfo_children():
            if isinstance(widget, tk.Label):
                widget.destroy()
        matches = self.station_adapter.search_station(query)  # Searching for stations matching the query
        if matches:
            # Displaying matching stations and their options
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
        # Method to handle genre search functionality
        search_window = tk.Toplevel(self.root)
        search_window.geometry("500x500")
        search_window.title("Search Genre")
        tk.Label(search_window, text="Enter the genre:").pack()
        search_entry = tk.Entry(search_window)
        search_entry.pack()
        search_entry.bind('<Return>', lambda event: self.display_genre_results(search_window, search_entry.get()))
        cancel_button = tk.Button(search_window, text="Cancel", command=search_window.destroy, width=20, height=2)
        cancel_button.pack(pady=5)

    # Method to display genre search results
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
                                               width=50, height=1,
                                               bd=2, relief=tk.RAISED, bg="lightgray",
                                               wraplength=200)
                    station_button.pack(pady=3, padx=10, fill=tk.X)
        else:
            tk.Label(scrollable_frame, text="No matching genres found.").pack()

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def display_genre(self):
        # Method to display genres
        genre_window = tk.Toplevel(self.root)
        genre_window.geometry("500x500")
        genre_window.title("Display Genre")
        # Creating a scrollable frame for displaying genres
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
        # Method to display stations for a given genre
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
                width=50, height=1,
                bd=2, relief=tk.RAISED, bg="lightgray",
                wraplength=200
            )
            station_button.pack(pady=3, padx=10, fill=tk.X)

            add_button = tk.Button(scrollable_frame, text="Add to Favorites",
                                   command=lambda s=station: self.add_to_favorites(s, self.stations[s]))
            add_button.pack(pady=3, padx=10, fill=tk.X)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        back_button = tk.Button(window, text="Back", command=go_back, width=20, height=2)
        back_button.pack(pady=10)

    def display_favorite_stations(self):
        # Method to display favorite stations
        fav_window = tk.Toplevel(self.root)
        fav_window.geometry("500x500")
        fav_window.title("Favorite Stations")
        favorites = self.favorites_manager.get_favorites()
        if favorites:
            # Displaying favorite stations and options
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
        # Method to remove a station from favorites
        self.favorites_manager.remove_from_favorites(station_name, station_url)  # Removing station from favorites
        self.display_favorite_stations()  # Refreshing display of favorite stations

    def add_to_favorites(self, station_name, station_url):
        # Method to add a station to favorites
        self.favorites_manager.add_to_favorites(station_name, station_url)
        self.display_favorite_stations()

    def display_recently_played(self):
        # Method to display recently played stations
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
        # Method to get station information
        station_name = self.stations.get(url)  # Getting station name from URL
        if station_name is None:
            station_name = url
        return station_name, url

    def play_radio(self, url):
        # Method to play radio station
        self.player.stop()  # Stopping currently playing station
        self.player = vlc.MediaPlayer(url)  # Loading new station URL into player
        self.player.play()  # Playing the station
        station_name, station_url = self.get_station_info(url)  # Getting station info
        self.recently_played_manager.add(station_name, station_url)  # Adding station to recently played list

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    RadioFacade().run()
