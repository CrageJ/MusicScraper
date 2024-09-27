import logging
import spotipy
from dotenv import load_dotenv
import os
from typing import List
from spotipy.oauth2 import SpotifyClientCredentials

def create_album_url(id):
    return f"https://open.spotify.com/album/{id}"

class SpotifyItem:
    def __init__(self, name: str, artists: List[str], release_date, total_tracks: int, spotify_id: str, genres: List[str], image_url):
        self.name = name
        self.artists = artists
        self.total_tracks = total_tracks
        self.spotify_id = spotify_id
        self.genres = genres
        self.release_date = release_date
        self.image_url = image_url

        # calculated attributes
        self.genre_list = self.create_genre_list()
        self.artist_list = self.create_artist_list()
        self.album_url = self.create_album_url()

    def create_genre_list(self):
        return ", ".join(self.genres)

    def create_artist_list(self):
        return ", ".join(self.artists)

    def create_album_url(self):
        return create_album_url(self.spotify_id)

    def __str__(self):
        return f"Album: {self.name}\nArtist(s): {self.artist_list}\nRelease Date: {self.release_date}\nTotal Tracks: {self.total_tracks}\nGenres: {self.genre_list}\nSpotify URL: {self.album_url}\nAlbum Art URL: {self.image_url}"


def compose_search_query(album, artist):
    return f"album:{album} artist:{artist}"

class Spotify:
    def __init__(self,connect=True):
        self.isConnected = connect
        self.client_id = "0"
        self.client_secret = "0"
        if connect:
            load_dotenv(".env")  # take environment variables from .env.
            self.client_id = os.getenv("SPOTIPY_CLIENT_ID")
            self.client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
            # redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")

            if not all([self.client_id, self.client_secret]):
                raise ValueError("Missing Spotify credentials in .env file")

            client_credentials_manager = SpotifyClientCredentials(client_id=self.client_id, client_secret=self.client_secret)
            self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)



    # search album is a lot less likely to return false info than get_artist_info. therefore, if search_album returns none, do not use info from get_artist_info
    def get_artist_info(self, artist):
        default = {"artist": artist, "genres": [], "id": 0}
        if not self.isConnected:
            return default
        try:
            response = self.sp.search(artist, limit=1, type="artist")
            if response is None:
                raise Exception("No response from Spotify API")
            artists = response["artists"]
            items = artists["items"]
            if len(items) > 0:
                item = items[0]
                genres = item["genres"]
                spotify_id = item["id"]
                return {"artist": artist, "genres": genres, "id": spotify_id}
        except Exception as e:
            logging.error(f"Error getting artist info for {artist}: {e}")
            return default
        return default

    def search_album(self, album, artist):
        default = SpotifyItem(album,[''],0,0,'',[''],'')
        if not self.isConnected:
            return default
        try:
            query = compose_search_query(album, artist)
            response = self.sp.search(query, type="album", limit=1)
            if response is None:
                raise Exception("No response from Spotify API")
            albums = response["albums"]["items"]
            if len(albums) > 0:
                album = albums[0]

                total_tracks = album["total_tracks"]
                name = album["name"]
                spotify_id = album["id"]
                artists = album["artists"]
                artists_names = [artist["name"] for artist in artists]
                artists = [self.get_artist_info(artist["name"]) for artist in artists]
                genres = [genre for artist in artists for genre in artist["genres"] if artist is not None]
                genres = list(set(genres))
                release_date = album["release_date"]
                album_image_url = album["images"][0]["url"] if album["images"] else ''
                spotifyItem = SpotifyItem(name, artists_names, release_date, total_tracks, spotify_id, genres, album_image_url)
                return spotifyItem
        except Exception as e:
            logging.error(f"Error searching for album {album} by {artist}: {e}")
            return default
        return default
