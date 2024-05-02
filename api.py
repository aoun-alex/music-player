from googleapiclient.discovery import build

#Factory

class ServiceFactory:
    @staticmethod
    def get_service(service_name):
        if service_name == 'youtube':
            return build('youtube', 'v3', developerKey='AIzaSyDmfZIO9hgun_GfTarU33Z_pkY5bc--Qio')
        else:
            raise ValueError("Invalid service name")


def search(query):
    # Building a YouTube API service object using the factory
    youtube = ServiceFactory.get_service('youtube')

    # Creating a search request
    request = youtube.search().list(
        part='snippet',
        maxResults=5,
        q=query,
        type='video'
    )

    response = request.execute()

    # Extracting relevant information from the response
    results = [{'title': item['snippet']['title'], 'videoId': item['id']['videoId']} for item in response['items']]

    return results
