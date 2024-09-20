from typing_extensions import List, Optional
import typing

from src.scraping.scraper import *
import cloudscraper
from bs4 import BeautifulSoup
import io

class BestEverAlbums(Scraper):
    def __init__(self):
        super().__init__(
            Website.BEA,
            "Best Ever Albums",
            "https://www.besteveralbums.com/yearstats.php?y={year}&f=&fv=&orderby=InfoRankScore&sortdir=DESC&page={page}",
            10,1)

    def parse_html(self,response:str) -> Optional[List[Album]]: # page at 0
        try:
            #get_html() -> str
            # Assuming the HTML content is stored in a variable called 'html_content'
            html_content = open("out.html","r",encoding='utf-8')
            soup = BeautifulSoup(html_content, 'html.parser')

            # Find all album list rows
            album_rows = soup.find_all('div', class_='albumListRow')

            albums = []

            for row in album_rows:
                album = {}

                # Extract rank
                rank = row.find('span', class_='albumListRank').text.strip().rstrip('.')

                album_rank = int(rank)

                # Extract title and artist
                title_element = row.find('h2', class_='albumListTitle')

                album_name = title_element.find('a').text.strip()

                # Extract release date
                album_release_date = row.find('div', class_='albumListDate').text.strip()
                album_score = 0

                # Extract user score
                score_container = row.find('div', class_='albumListScoreContainer')
                if score_container:
                    score = score_container.find('div', class_='scoreValue').text.strip()
                    album_score = int(score)

                    #ratings = score_container.find('div', class_='scoreText').text.strip()
                    #album['ratings'] = ratings

                album = ()
                albums.append(album)
            return albums
        except Exception as e:
            print(e)
            return None
