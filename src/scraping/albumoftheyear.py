from typing_extensions import List, Optional
import typing
from src.scraping.scraper import *
import cloudscraper
from bs4 import BeautifulSoup
import io

class AlbumOfTheYear(Scraper):
    def __init__(self):
        super().__init__(
            Website.ALBUMOFTHEYEAR,
            "Album of the Year",
            "https://www.albumoftheyear.org/ratings/user-highest-rated/{year}/{page}/",
            25,1)


    def parse_html(self,response:str) ->List[Album]: # page at 0
        if not response:
            return []
        try:
            #get_html() -> str
            # Assuming the HTML content is stored in a variable called 'html_content'

            soup = BeautifulSoup(response, 'html.parser')

            # Find all album list rows
            album_rows = soup.find_all('div', class_='albumListRow')

            albums = []

            for row in album_rows:

                # Extract rank
                rank = row.find('span', class_='albumListRank').text.strip().rstrip('.')

                album_rank = int(rank)

                # Extract title and artist
                title_element = row.find('h2', class_='albumListTitle')

                album_str = title_element.find('a').text.strip()
                print("ALBUM STR: ",album_str)
                album_str = album_str.split(' - ')
                album_name = album_str[1]
                album_artist = album_str[0]


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
                album = Album(album_name,album_artist,rank,album_score,Website.ALBUMOFTHEYEAR)
                albums.append(album)
            return albums
        except Exception as e:
            print(e)
            return []
