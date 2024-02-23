from googleapiclient.discovery import build


def search(query):
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
