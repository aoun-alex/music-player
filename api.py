from googleapiclient.discovery import build  # Importing build function from googleapiclient.discovery
from abc import ABC, abstractmethod  # Importing ABC and abstractmethod for creating abstract classes


# Abstract class for API commands
class APICommand(ABC):
    @abstractmethod
    def execute(self, query):
        pass


# Concrete command class for executing search queries
class SearchCommand(APICommand):
    def execute(self, query):
        # Building a YouTube API service object
        youtube = build('youtube', 'v3', developerKey='AIzaSyDmfZIO9hgun_GfTarU33Z_pkY5bc--Qio')

        # Creating a search request
        request = youtube.search().list(
            part='snippet',
            maxResults=5,
            q=query,
            type='video'
        )

        # Executing the search request
        response = request.execute()

        # Extracting relevant information from the response
        results = [{'title': item['snippet']['title'], 'videoId': item['id']['videoId']} for item in response['items']]

        return results


# Factory class for creating API commands
class APIFactory:
    @staticmethod
    def create_api(type):
        if type == "Search":
            return SearchCommand()


# Function to perform a search using the YouTube API
def search(query):
    return APIFactory.create_api("Search").execute(query)
