import csv
from fuzzywuzzy import process
import time


def load_stations(filename):
    stations = {}
    genres = {}
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            name, genre, url = row
            stations[name] = url
            for single_genre in genre.split(','):
                single_genre = single_genre.strip()  # remove leading/trailing spaces
                if single_genre not in genres:
                    genres[single_genre] = []
                genres[single_genre].append(name)
    return stations, genres


def search_station(stations, query):
    matches = process.extractBests(query.lower(), {station.lower(): station for station in stations.keys()}, limit=10)
    if matches:
        return [(original_name, stations[original_name]) for original_name, _, _ in matches]
    else:
        return []

def search_genre(genres, query):
    matches = process.extractBests(query.lower(), {g.lower(): g for g in genres.keys()}, limit=10)
    if matches:
        return [(original_genre, genres[original_genre]) for original_genre, _, _ in matches]
    else:
        return []


def display_genres(genres):
    print("Available genres:")
    for genre in genres:
        print(genre)


def main():
    stations, genres = load_stations('stations.csv')

    while True:
        print("1. Search station")
        print("2. Search genre")
        print("3. Display genres")
        print("4. Quit")
        choice = input("Enter your choice: ")

        if choice == '1':
            search_station(stations)
        elif choice == '2':
            search_genre(genres)
        elif choice == '3':
            display_genres(genres)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Try again.")

        time.sleep(1)


if __name__ == "__main__":
    main()
