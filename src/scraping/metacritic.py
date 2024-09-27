
from typing_extensions import List, Optional
import typing

from src.scraping.scraper import *
import cloudscraper
from bs4 import BeautifulSoup
import io

class MetaCritic(Scraper):
    def __init__(self):
        super().__init__(
            Website.META,
            "Metacritic",
            "https://www.metacritic.com/browse/albums/score/metascore/year/filtered?year_selected={year}&distribution=&sort=desc&view=detailed&page={page}",
            100,
            0)



    def parse_html(self,response:str) -> List[Album]: # page at 0
        if response == '':
            return []
        try:
            # Assuming the HTML content is stored in a variable called 'html_content'
            soup = BeautifulSoup(response, 'html.parser')

            albums = []

            for item in soup.find_all('div', class_='item'):
                try:
                    album = {}

                    # Extract title
                    title_elem = item.find('div', class_='title')
                    title = ''
                    if title_elem:
                        title = title_elem.text.strip()
                    # Extract rank
                    rank = 0
                    rank_elem = item.find('span', class_='title numbered')
                    if rank_elem:
                        rank = rank_elem.text.strip().rstrip('.')

                    # Extract artist
                    artist_elem = item.find('div', class_='artist')
                    artist = ''
                    if artist_elem:
                        artist = artist_elem.text.strip()

                    rating = 0
                    # Extract User Score
                    user_score_elem = item.find('span', class_='metascore_w user')
                    if user_score_elem:
                        rating = user_score_elem.text.strip()

                    a = Album(title, artist, rank, rating, Website.META)

                    albums.append(album)
                except Exception as e:
                    logging.error(f"Error parsing album: {e}")
                    continue
            return albums
        except Exception as e:
            logging.error(f"Error parsing album: {e}")
            return []
