import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import webbrowser

class Music:
    def __init__(self, name, link):
        self.name = name
        self.link = link

    def __str__(self):
        return f"{self.name}: {self.link}"

client_id = 'SEU_CLIENT_ID'
client_secret = 'SEU_CLIENT_SECRET'

# Lê o conteúdo do arquivo id.txt e armazena na variável client_id
with open("id.txt", "r") as file:
    client_id = file.read().strip()

# Lê o conteúdo do arquivo secret.txt e armazena na variável client_secret
with open("secret.txt", "r") as file:
    client_secret = file.read().strip()

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Busca as músicas da Taylor Swift
artist_name = 'Taylor Swift'
result = sp.search(artist_name, type='artist')
artist_uri = result['artists']['items'][0]['uri']

results = sp.artist_albums(artist_uri, album_type='album')
albums = results['items']
while results['next']:
    results = sp.next(results)
    albums.extend(results['items'])

tracks = []
for album in albums:
    results = sp.album_tracks(album['uri'])
    tracks.extend(results['items'])

# Escolhe uma música aleatória
random_track = random.choice(tracks)
music = Music(random_track['name'], random_track['external_urls']['spotify'])
webbrowser.open(music.link)
