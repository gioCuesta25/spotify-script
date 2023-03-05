import os
import json
from dotenv import load_dotenv
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth

load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
redirect_uri = 'https://github.com/Giovanni-Romana-Cuesta'

authorization_base_url = "https://accounts.spotify.com/authorize"
token_url = 'https://accounts.spotify.com/api/token'
scope = [
    'user-read-email', 'playlist-read-collaborative', 'user-read-private', 'playlist-read-private',
    'user-library-modify', 'user-library-read'
]

spotify = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)
authorization_url, state = spotify.authorization_url(authorization_base_url)

print('Please go here and authorize: ', authorization_url)

redirect_response = input('\n\nPaste the full redirect URL here:')

auth = HTTPBasicAuth(client_id, client_secret)

token = spotify.fetch_token(token_url, auth=auth, authorization_response=redirect_response)

r = spotify.get('https://api.spotify.com/v1/me/playlists?limit=25')

content = json.loads(r.content)

playlist_name = ''
playlist_id = ''
tracks = []

for item in content['items']:
    if item['name'] == 'My list':
        playlist_name = 'My  list'
        playlist_id = item['id']
        tracks = item['tracks']

total_songs = tracks['total']
offset = 0
has_more = True
url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks?limit=50&offset={offset}'

while has_more:
    res = spotify.get(url=url)
    playlist_items = json.loads(res.content)
    tracks_ids = []

    for item in playlist_items['items']:
        info = item['track']
        tracks_ids.append(info['id'])

    res = spotify.put('https://api.spotify.com/v1/me/tracks',
                      json={'ids': tracks_ids},
                      headers={'Content-Type': 'application/json'})

    if playlist_items['next'] is None:
        has_more = False

    url = playlist_items['next']
