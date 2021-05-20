import os
import spotipy
import time
from spotipy.oauth2 import SpotifyOAuth


def auth_sp():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv('SPOTIPY_CLIENT_ID'),
                                                   client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
                                                   redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI'),
                                                   scope="user-read-currently-playing,user-top-read"
                                                   ))
    return sp


def current_track(spotify_client):
    last_song_name = ''
    last_artist_name = ''
    while (True):
        results_me = spotify_client.currently_playing()

        current_song_name = results_me['item']['name']
        current_artist_name = results_me['item']['artists'][0]['name']

        song_percent = results_me['progress_ms'] / results_me['item']['duration_ms']

        if (last_artist_name != current_artist_name) & (last_song_name != current_song_name) & (song_percent >= 0.3):
            print('Now playing: ', current_artist_name, ' - ', current_song_name)
            last_artist_name = current_artist_name
            last_song_name = current_song_name

        time.sleep(10)


def top_artists(spotify_client):
    descr_range = {
        'short_term': "last month",
        'medium_term': "last 6 month",
        'long_term': "all time",
    }
    # Подробное описание типов
    # https://developer.spotify.com/documentation/web-api/reference/#endpoint-get-users-top-artists-and-tracks

    limit = 5

    ranges = ['short_term', 'medium_term', 'long_term']
    for sp_range in ranges:
        print("My top artist for", descr_range.get(sp_range, "Invalid month"), ':')
        results = spotify_client.current_user_top_artists(time_range=sp_range, limit=limit)

        for i, item in enumerate(results['items']):
            print(
                i,
                item['name']
            )
        print()


def top_tracks(spotify_client):
    descr_range = {
        'short_term': "last month",
        'medium_term': "last 6 month",
        'long_term': "all time",
    }
    # Подробное описание типов
    # https://developer.spotify.com/documentation/web-api/reference/#endpoint-get-users-top-artists-and-tracks

    limit = 5

    ranges = ['short_term', 'medium_term', 'long_term']
    for sp_range in ranges:
        print("My top songs for", descr_range.get(sp_range, "Invalid month"), ':')
        results = spotify_client.current_user_top_tracks(time_range=sp_range, limit=limit)

        for i, item in enumerate(results['items']):
            print(
                i,
                item['artists'][0]['name'],
                '-', item['name']
            )
        print()


if __name__ == '__main__':
    spotify_client = auth_sp()
    current_track(spotify_client)
    top_tracks(spotify_client)
    top_artists(spotify_client)
