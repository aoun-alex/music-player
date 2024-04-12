import json
import os
from abc import ABC, abstractmethod

#Strategy

class StorageManager(ABC):
    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def save(self, data):
        pass


class JSONStorageManager(StorageManager):
    def __init__(self, file_name):
        # Constructor method for JSONStorageManager class
        self.file_name = file_name

    def load(self):
        # Method to load data from JSON file
        if os.path.exists(self.file_name):
            with open(self.file_name, 'r') as f:
                return json.load(f)
        return []

    def save(self, data):
        # Method to save data to JSON file
        with open(self.file_name, 'w') as f:
            json.dump(data, f)


class FavoritesManager:
    def __init__(self, storage_manager):
        # Constructor method for FavoritesManager class
        self.storage_manager = storage_manager  # Initializing storage manager
        self.favorites = self.storage_manager.load()

    def add_to_favorites(self, station_name, station_url):
        # Method to add a station to favorites
        if (station_name, station_url) not in self.favorites:
            self.favorites.append((station_name, station_url))
            self.storage_manager.save(self.favorites)

    def remove_from_favorites(self, station_name, station_url):
        # Method to remove a station from favorites
        if (station_name, station_url) in self.favorites:
            self.favorites.remove((station_name, station_url))
            self.storage_manager.save(self.favorites)

    def get_favorites(self):
        # Method to get the list of favorite stations
        return self.favorites

    def clear_favorites(self):
        # Method to clear all favorite stations
        self.favorites = []
        self.storage_manager.save(self.favorites)
