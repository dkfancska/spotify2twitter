import os
import spotipy
import time
from spotipy.oauth2 import SpotifyOAuth


def auth_sp():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv('SPOTIPY_CLIENT_ID'),
                                                   client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
                                                   redirect_uri=os.getenv(
                                                       'SPOTIPY_REDIRECT_URI=http://localhost:8888/callback/'),
                                                   scope="user-read-currently-playing"
                                                   ))
    return sp


def current_track():
    spotipy_client = auth_sp()
    last_song_name = ''
    last_artist_name = ''
    while (True):
        results_me = spotipy_client.currently_playing()

        current_song_name = results_me['item']['name']
        current_artist_name = results_me['item']['artists'][0]['name']

        song_percent = results_me['progress_ms'] / results_me['item']['duration_ms']

        if (last_artist_name != current_artist_name) & (last_song_name != current_song_name) & (song_percent >= 0.3):
            print('Now playing: ' + current_artist_name + ' - ' + current_song_name)
            last_artist_name = current_artist_name
            last_song_name = current_song_name

        time.sleep(10)

if __name__ == '__main__':
    current_track()