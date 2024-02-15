from googleapiclient.discovery import build
from abc import ABC, abstractmethod


class APICommand(ABC):
    @abstractmethod
    def execute(self, query):
        pass


class SearchCommand(APICommand):
    def execute(self, query):
        youtube = build('youtube', 'v3', developerKey='AIzaSyDmfZIO9hgun_GfTarU33Z_pkY5bc--Qio')

        request = youtube.search().list(
            part='snippet',
            maxResults=5,
            q=query,
            type='video'
        )

        response = request.execute()

        results = [{'title': item['snippet']['title'], 'videoId': item['id']['videoId']} for item in response['items']]

        return results


class APIFactory:
    @staticmethod
    def create_api(type):
        if type == "Search":
            return SearchCommand()
        else:
            raise ValueError("Invalid API type")


def api_decorator(func):
    def wrapper(*args, **kwargs):
        print("Starting API operation...")
        result = func(*args, **kwargs)
        print("API operation finished!")
        return result

    return wrapper


@api_decorator
def search(query):
    return APIFactory.create_api("Search").execute(query)
