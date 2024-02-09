from api import YouTubeAPI
import webbrowser


def main():
    api_key = "AIzaSyDmfZIO9hgun_GfTarU33Z_pkY5bc--Qio"
    youtube_api = YouTubeAPI(api_key)

    # Ask user for search query
    search_query = input("Please input your search query: ")

    # Search for videos
    videos = youtube_api.search_videos(search_query)

    # Display search results
    print("Search results:")
    for i, video in enumerate(videos, start=1):
        print(f"{i}. {video['title']}")

    # Prompt user to select a video
    selection = input("Select a video (1-5): ")
    try:
        selection_index = int(selection) - 1
        if 0 <= selection_index < len(videos):
            selected_video = videos[selection_index]
            video_url = youtube_api.get_video_url(selected_video["video_id"])
            print(f"Opening video: {selected_video['title']}")
            webbrowser.open(video_url)
        else:
            print("Invalid selection. Please select a number between 1 and 5.")
    except ValueError:
        print("Invalid input. Please enter a number.")


if __name__ == "__main__":
    main()
