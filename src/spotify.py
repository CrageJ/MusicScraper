import spotipy
from dotenv import load_dotenv
import os
from typing import List

class SpotifyItem:
    def __init__(self,name:str,artists:List[str],release_date,total_tracks:int,spotify_id:str,genres:List[str]):
        self.name = name
        self.artists = artists
        self.total_tracks = total_tracks
        self.spotify_id = spotify_id
        self.genres = genres
        self.release_date = release_date

class Spotify:
    def __init__(self):
        load_dotenv(".env")  # take environment variables from .env.
        SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
        SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
        SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
        self.sp = spotipy.Spotify(auth_manager=spotipy.SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET))

    def compose_search_query(self,album,artist):
        return f"album:{album} artist:{artist}"

    def get_album_url(self,spotifyID):
        return f"https://open.spotify.com/album/{spotifyID}"

    def get_artist_info(self,artist):
        response = self.sp.search(artist,limit=1,type="artist")
        artists = getattr(response,"artists")
        items = getattr(artists,"items")
        if len(items) > 0:
            item = items[0]
            genres = getattr(item,"genres")
            spotify_id = getattr(item,"id")
            return {"genres":genres,"id":spotify_id}

        return {"genres":[],"id":0}

    def search_album(self,album,artist):
        query = self.compose_search_query(album,artist)
        response = self.sp.search(query,type="album",limit=1)
        albums = getattr(response,"albums")
        items = getattr(albums,"items")
        if len(items) > 0:
            album = items[0]

            total_tracks = getattr(album,"total_tracks")
            name = getattr(album,"name")
            spotify_id = getattr(album,"id")
            artists = getattr(album,"artists")
            artists = [getattr(artist,"name") for artist in artists]
            genres = [genre for artist in artists for genre in self.get_artist_info(artist)["genres"]]
            genres = list(set(genres))
            release_date = getattr(album,"release_date")
            spotifyItem = SpotifyItem(name,artists,release_date,total_tracks,spotify_id,genres)
            return spotifyItem
        else:
            return None

        return result
