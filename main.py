import requests


def get_video_id(query):
    url = (f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=5&q={query}&type=video&key"
           f"=AIzaSyDmfZIO9hgun_GfTarU33Z_pkY5bc--Qio")
    response = requests.get(url)
    data = response.json()
    video_ids = []
    for item in data['items']:
        video_ids.append(f"https://www.youtube.com/watch?v={item['id']['videoId']}")
    return video_ids


def main():
    query = input("Enter your search query: ")
    video_ids = get_video_id(query)
    for video_id in video_ids:
        print(video_id)


if __name__ == "__main__":
    main()
