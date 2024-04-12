import json
import os

#Flyweight

class Station:
    def __init__(self, name, url):
        # Constructor method for Station class
        self.name = name
        self.url = url


class StationFactory:
    def __init__(self):
        # Constructor method for StationFactory class
        self._stations = {}

    def get_station(self, name, url):
        # Method to get or create a station instance
        if (name, url) not in self._stations:
            self._stations[(name, url)] = Station(name, url)
        return self._stations[(name, url)]


class RecentlyPlayed:
    def __init__(self, factory, file_path='recently_played.json'):
        # Constructor method for RecentlyPlayed class
        self.file_path = file_path
        self.recently_played = []
        self.factory = factory
        self.load()

    def load(self):
        # Method to load recently played stations from file
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                stations = json.load(file)
                # Creating Station instances for each loaded station and adding them to recently_played list
                self.recently_played = [self.factory.get_station(name, url) for name, url in stations]
        else:
            self.recently_played = []  # Initializing recently_played list if file doesn't exist

    def save(self):
        # Method to save recently played stations to file
        with open(self.file_path, 'w') as file:
            stations = [(station.name, station.url) for station in self.recently_played]
            json.dump(stations, file)

    def add(self, station_name, station_url):
        # Method to add a station to recently played list
        station = self.factory.get_station(station_name, station_url)
        self.recently_played.insert(0, station)
        if len(self.recently_played) > 5:
            self.recently_played.pop()  # Removing the oldest station if the list is longer than 5
        self.save()

    def get_recently_played(self):
        # Method to get recently played stations
        return [(station.name, station.url) for station in self.recently_played]
