from typing_extensions import List, Optional
import typing

from src.scraping.scraper import *
import cloudscraper
from bs4 import BeautifulSoup
import io
import re
class BestEverAlbums(Scraper):
    def __init__(self):
        super().__init__(
            Website.BEA,
            "Best Ever Albums",
            "https://www.besteveralbums.com/yearstats.php?y={year}&f=&fv=&orderby=InfoRankScore&sortdir=DESC&page={page}",
            10,1)

    def parse_html(self,response:str) -> List[Album]: # page at 0
        if response == '':
            return []
        try:
            soup = BeautifulSoup(response, 'html.parser')
            albums = []

            for rank, album_div in enumerate(soup.find_all('div', class_='chartrow'), 1):
                try:
                    # Album title
                    title_elem = album_div.find('a', class_='nav2emph bigger')
                    title = ''
                    if title_elem:
                        title = title_elem.text.strip()

                    # Artist
                    artist_elem = album_div.find('div', class_='chart-title-col chartstring').find('a', class_='nav2emph bigger')
                    artist = ''
                    if artist_elem:
                        artist = artist_elem.text.strip()

                    rank = 0
                    average_rating = 0

                    # Additional stats
                    stats_div = album_div.find('div', class_='chart-stats')
                    if stats_div:
                        for stat in stats_div.find_all('div', class_='chartstring'):
                            key = stat.text.strip(':')
                            value = stat.find_next_sibling('div', class_='chart-stats-metric')
                            if value:
                                value = value.text.strip()
                                if key == 'Overall Rank':
                                    rank = value.split()[-1]
                                elif key == 'Average Rating':
                                    parts = value.split()
                                    if len(parts) >= 2:
                                        average_rating = parts[0]
                    album = Album(title, artist, rank, average_rating, Website.BEA)
                    albums.append(album)
                except Exception as e:
                    logging.error(f"Error parsing album: {e}")
                    continue
            return albums

        except Exception as e:
            logging.error(f"Error parsing album: {e}")
            return []
