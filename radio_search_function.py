import csv
from fuzzywuzzy import process

#Adapter

class StationAdapter:
    def __init__(self, filename):
        # Constructor method for StationAdapter class
        self.stations, self.genres = self.load_stations(filename)

    def load_stations(self, filename):
        # Method to load stations and genres from a CSV file
        stations = {}
        genres = {}
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                name, genre, url = row
                stations[name] = url
                for single_genre in genre.split(','):
                    single_genre = single_genre.strip()
                    if single_genre not in genres:
                        genres[single_genre] = []
                    genres[single_genre].append(name)
        return stations, genres

    def search_station(self, query):
        # Method to search for a station based on a query
        matches = process.extractBests(query.lower(), {station.lower(): station for station in self.stations.keys()},
                                       limit=10)
        if matches:
            return [(original_name, self.stations[original_name]) for original_name, _, _ in matches]  # Returning matched station names and URLs
        else:
            return []

    def search_genre(self, query):
        # Method to search for a genre based on a query
        matches = process.extractBests(query.lower(), {g.lower(): g for g in self.genres.keys()}, limit=10)
        if matches:
            return [(original_genre, self.genres[original_genre]) for original_genre, _, _ in matches]
        else:
            return []
