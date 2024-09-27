from src.scraping.scraper import Album, Scraper
import src.scraping.albumoftheyear as AOTY
import src.scraping.besteveralbums as BEA
import src.scraping.rateyourmusic as RYM
import src.scraping.metacritic as META
import src.spotify as SPOTIFY
import src.database as DB

from typing import Any, List

import logging

from src.utils import Website


# handles all data processing, NOT website backend
class Application:
    def __init__(self,db = ''):
        self.db = DB.Database(db)
        self.aoty = AOTY.AlbumOfTheYear()
        self.bea = BEA.BestEverAlbums()
        self.rym = RYM.RateYourMusic()
        self.meta = META.MetaCritic()
        self.spotify = SPOTIFY.Spotify()

        self.scraper_list : List[Any] = [self.aoty,self.bea,self.rym,self.meta]
        self.scraper_list_str = [Website.AOTY,Website.BEA,Website.RYM,Website.META]
        # Initialize logger
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        self.logger.info("Application Started")

    async def async_init(self):
        await self.db.async_init()

    async def scrape_websites(self, top_x, from_year, to_year,
                            aoty=False, bea=False, rym=False, meta=False, rescrape_old_data=False):
        logging.info ("Scraping websites")
        args = [aoty, bea, rym, meta]
        for arg, s, scraper in zip(args, self.scraper_list_str, self.scraper_list):
            if arg:
                self.logger.info(f"Scraping {s}")
                # In the format (website, [(year, [html_content, ...]), ...])
                raw_data = scraper.scrape_top_x_between_years(top_x, from_year, to_year, rescrape_old_data)
                for tup in raw_data:
                    year, pages = tup
                    for page in pages:
                        if page == '':
                            continue

                        parsed_content : List[Album]= scraper.parse_html(page)
                        for album in parsed_content:

                            album_name = album.album
                            artist = album.artist
                            rank = album.rank
                            rating = album.rating
                            website = album.website

                            spotify_info : SPOTIFY.SpotifyItem= self.spotify.search_album(album_name, artist)
                            if spotify_info is not None:
                                sp_album = spotify_info.name
                                sp_id = spotify_info.spotify_id
                                sp_artists = spotify_info.artists
                                sp_total_tracks = spotify_info.total_tracks
                                sp_genres = spotify_info.genres
                                sp_release_date = spotify_info.release_date
                                sp_image_url = spotify_info.image_url

                                await self.db.insert_spotify(sp_id, sp_album, ", ".join(sp_artists),", ".join(sp_genres), sp_release_date, sp_image_url)
                                await self.db.insert_text_to_spotify(album_name, artist, sp_id)

                            await self.db.insert_album(website, year, rank, album_name, artist)


    async def get_content(self, top_x, from_year, to_year,
                                  aoty=False, bea=False, rym=False, meta=False):
        logging.info ("Getting Content")
        result = []
        websites = []
        if aoty:
            websites.append(Website.AOTY)
        if bea:
            websites.append(Website.BEA)
        if rym:
            websites.append(Website.RYM)
        if meta:
            websites.append(Website.META)

        # Get albums from the specified range and top_x
        albums = await self.db.get_albums_range_top_x(from_year, to_year, top_x)

        if albums is not None:
            for album in albums:
                try:
                    website, year, rank, album_name, artist,genres,release_date,img_url = album

                    # Get Spotify information
                    spotify_info = await self.db.get_spotify(album_name, artist)

                    album_data = {
                        "website": website,
                        "year": year,
                        "rank": rank,
                        "album": album_name,
                        "artist": artist,
                        "img_url": img_url,
                        "spotify": None
                    }

                    if spotify_info:
                        spotify_id, sp_album, sp_artist, genres, release_date, image_url = spotify_info
                        album_data["spotify"] = {
                            "id": spotify_id,
                            "album": sp_album,
                            "artist": sp_artist,
                            "genres": genres,
                            "release_date": release_date,
                            "image_url": image_url
                        }
                except Exception as e:
                    logging.error(f"Error in getting content: {e}")
                    continue

                result.append(album_data)

            # Sort the result by year and rank
            result.sort(key=lambda x: (x["year"], x["rank"]))

            return result

    async def get_aggregated_content(self, top_x, from_year, to_year,
                                    aoty=True, bea=True, rym=True, meta=True):
        logging.info ("Getting Aggregated Content")
        result = []
        websites = []
        if aoty:
            websites.append(Website.AOTY)
        if bea:
            websites.append(Website.BEA)
        if rym:
            websites.append(Website.RYM)
        if meta:
            websites.append(Website.META)

        # Get aggregated albums from the specified range
        albums = await self.db.get_albums_aggregated(from_year, to_year)

        if albums:
            for album in albums:
                album_name, artist, website_count, average_rank, year, genres, release_date, img_url = album

                album_data = {
                    "album": album_name,
                    "artist": artist,
                    "website_count": website_count,
                    "average_rank": average_rank,
                    "year": year,
                    "genres": genres,
                    "release_date": release_date,
                    "img_url": img_url,
                    "websites": []
                }

                result.append(album_data)

            # Sort the result by average rank and website count
            result.sort(key=lambda x: (x["average_rank"], -x["website_count"]))

            # Limit to top_x results
            return result[:top_x]

        return []
