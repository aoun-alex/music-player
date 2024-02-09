from googleapiclient.discovery import build
from urllib.parse import urlencode


class YouTubeAPI:
    def __init__(self, api_key):
        self.api_service_name = "youtube"
        self.api_version = "v3"
        self.api_key = api_key
        self.youtube = build(self.api_service_name, self.api_version, developerKey=self.api_key)

    def search_videos(self, query, max_results=5):
        search_response = self.youtube.search().list(
            q=query,
            part="snippet",
            maxResults=max_results
        ).execute()

        videos = []
        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
                video_id = search_result["id"]["videoId"]
                title = search_result["snippet"]["title"]
                videos.append({"title": title, "video_id": video_id})

        return videos

    def get_video_url(self, video_id):
        base_url = "https://www.youtube.com/watch?"
        params = {"v": video_id}
        video_url = base_url + urlencode(params)
        return video_url
