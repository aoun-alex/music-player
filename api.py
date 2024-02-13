from googleapiclient.discovery import build


def search(query):
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
