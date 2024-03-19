import vlc
import time

def main():
    # Define a list of radio stations with their names and URLs
    stations = [
        {"name": "Radio Paradise", "url": "http://stream.radioparadise.com/rock-192"},
        {"name": "NPR News", "url": "https://npr-ice.streamguys1.com/live.mp3"},
        {"name": "KEXP 90.3 FM", "url": "https://kexp-mp3-128.streamguys1.com/kexp128.mp3"},
        {"name": "SomaFM Groove Salad", "url": "https://ice4.somafm.com/groovesalad-128-mp3"},
        {"name": "FIP", "url": "http://direct.fipradio.fr/live/fip-midfi.mp3"},
        {"name": "Radio Swiss Jazz", "url": "http://stream.srg-ssr.ch/m/rsj/mp3_128"},
    ]

    while True:  # Keep the program running until the user decides to exit
        # Print station names to the console
        print("Available radio stations:")
        for i, station in enumerate(stations, start=1):
            print(f"{i}. {station['name']}")

        # Ask the user to choose a station
        choice = input("Enter the number of the station you want to listen to, or 'q' to quit: ")

        if choice.lower() == 'q':
            break  # Exit the program

        choice = int(choice)

        # Validate user input
        if choice < 1 or choice > len(stations):
            print("Invalid choice. Try again.")
            continue

        # Get the URL of the selected station
        selected_station = stations[choice - 1]
        station_url = selected_station["url"]

        # Play the selected station
        print(f"Playing {selected_station['name']}")
        player = vlc.MediaPlayer(station_url)
        player.play()

        while True:  # Keep the music playing until the user decides to stop
            stop = input("Press 's' to stop the music and choose another station, or 'q' to quit: ")
            if stop.lower() == 's':
                player.stop()
                break
            elif stop.lower() == 'q':
                return  # Exit the program

        time.sleep(1)  # Wait for a second before the next iteration

if __name__ == "__main__":
    main()