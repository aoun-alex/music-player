import json
import os

#Proxy

class JSONStorageProxy:
    def __init__(self, file_name):
        self.file_name = file_name

    def load(self):
        if os.path.exists(self.file_name):
            with open(self.file_name, 'r') as f:
                return json.load(f)
        return []

    def save(self, data):
        with open(self.file_name, 'w') as f:
            json.dump(data, f)


class FavoritesManager:
    def __init__(self, storage_proxy):
        self.storage_proxy = storage_proxy
        self.favorites = self.storage_proxy.load()

    def add_to_favorites(self, station_name, station_url):
        if (station_name, station_url) not in self.favorites:
            self.favorites.append((station_name, station_url))
            self.storage_proxy.save(self.favorites)

    def remove_from_favorites(self, station_name, station_url):
        if (station_name, station_url) in self.favorites:
            self.favorites.remove((station_name, station_url))
            self.storage_proxy.save(self.favorites)

    def get_favorites(self):
        return self.favorites

    def clear_favorites(self):
        self.favorites = []
        self.storage_proxy.save(self.favorites)
