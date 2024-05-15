# Music player architecture
## Main app
mainapp.py

## Youtube Importer Module
**youtube_importer.py** - BUILDER (the main menu app for the youtube importer)

**song_menu.py** - PROTOTYPE (the music player that plays songs from the users pc)

**download_page.py** - ABSTRACT FACTORY (the song downloader that downloads songs from youtube)

**api.py** - FACTORY (the api file that contains the youtube api)

## Radio Player Module:
**radio_player.py** - FACADE (the main menu app for the radio player)

**radio_search_function.py** - ADAPTER (the function that adds the search ability to search different radio stations)

**recently_played.py** - FLYWEIGHT (a function that shows recently played radio stations)

**radio_favorites.py** - PROXY (a favorite stations function)

## Spotify Recommender Module:
**recommender_main.py** - STATE (the main recommender app)

**ai_recommender.py** - STRATEGY (uses an api to recommend spotify songs)

**song_downloader.py** - TEMPLATE METHOD (function to download songs from spotify)

**ai_downloader_helper.py** - COMMAND (helper function to download songs from spotify)

