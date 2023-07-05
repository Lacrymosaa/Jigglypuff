import sys
import json
import random
import webbrowser
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt

class Music:
    def __init__(self, name, link):
        self.name = name
        self.link = link

    def __str__(self):
        return f"{self.name}: {self.link}"

class Jigglypuff(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Jigglypuff')
        self.setGeometry(300, 300, 250, 100)
        self.setStyleSheet("background-color: #F0D2DB;")

        icon = QIcon("srcs/Jigglypuff.ico")
        self.setWindowIcon(icon)
        
        font = QFont("Cascadia Mono", 12, QFont.Bold)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 1)
        self.artist_label = QLabel('Artist Name:', self)
        self.artist_label.setFont(font)
        
        self.artist_input = QLineEdit(self)
        self.artist_input.setStyleSheet("border: 1px solid #000; background-color: #fff;")

        self.random_button = QPushButton('Play!', self)
        self.random_button.clicked.connect(self.play_random_music)
        self.random_button.setStyleSheet("QPushButton {"
                                          "background-color: #FFB6C1;"
                                          "border: 1px solid black;"
                                          "border-radius: 1px;"
                                          "padding: 5px;"
                                          "font-size: 14px;"
                                          "letter-spacing: 1px;"
                                          "}"
                                          "QPushButton:hover {"
                                          "background-color: #FFC0CB;"
                                          "}"
                                          "QPushButton:pressed {"
                                          "background-color: #FFA07A;"
                                          "}")

        vbox = QVBoxLayout()
        vbox.addWidget(self.artist_label)
        vbox.addWidget(self.artist_input)
        vbox.addWidget(self.random_button)

        self.setLayout(vbox)
        self.show()

    def play_random_music(self):
        artist_name = self.artist_input.text()

        client_id = 'SEU_CLIENT_ID'
        client_secret = 'SEU_CLIENT_SECRET'

        # Lê as credenciais do arquivo JSON
        with open("credentials.json", "r") as file:
            credentials = json.load(file)

        client_id = credentials["client_id"]
        print(client_id)
        client_secret = credentials["client_secret"]
        print(client_secret)

        client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

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

        if tracks:
            random_track = random.choice(tracks)
            music = Music(random_track['name'], random_track['external_urls']['spotify'])
            webbrowser.open(music.link)
        else:
            print(f"No tracks found for the artist: {artist_name}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    music_app = Jigglypuff()
    sys.exit(app.exec_())
