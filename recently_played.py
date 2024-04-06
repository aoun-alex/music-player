import json
import os

class Station:
    def __init__(self, name, url):
        self.name = name
        self.url = url

class StationFactory:
    def __init__(self):
        self._stations = {}

    def get_station(self, name, url):
        if (name, url) not in self._stations:
            self._stations[(name, url)] = Station(name, url)
        return self._stations[(name, url)]

class RecentlyPlayed:
    def __init__(self, factory, file_path='recently_played.json'):
        self.file_path = file_path
        self.recently_played = []
        self.factory = factory
        self.load()

    def load(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                stations = json.load(file)
                self.recently_played = [self.factory.get_station(name, url) for name, url in stations]
        else:
            self.recently_played = []

    def save(self):
        with open(self.file_path, 'w') as file:
            stations = [(station.name, station.url) for station in self.recently_played]
            json.dump(stations, file)

    def add(self, station_name, station_url):
        station = self.factory.get_station(station_name, station_url)

        # Add the station to the start of the list
        self.recently_played.insert(0, station)

        # If the list is longer than 5, remove the oldest station
        if len(self.recently_played) > 5:
            self.recently_played.pop()

        self.save()

    def get_recently_played(self):
        return [(station.name, station.url) for station in self.recently_played]