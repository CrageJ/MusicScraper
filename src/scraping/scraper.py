from enum import Enum

from typing_extensions import List, Optional
import cloudscraper
from bs4 import BeautifulSoup
import io

from time import sleep
from typing import Optional
from dataclasses import dataclass


class Database:
    def __init__(self,name):
        self.name = name


class Proxies:
    def __init__(self,proxies):
        self.proxies = proxies
        self.current_proxy = 0
        self.proxy_count = len(proxies)


    def get_prox(self):
        """Automatically cycle through proxy each time"""
        # Get the proxies from the database
        ans = self.proxies[self.current_proxy]
        self.current_proxy += 1
        self.current_proxy %= self.proxy_count
        return ans

    def get_list(self):
        return self.proxies

class Website(Enum):
    UNDEFINED = 0,
    ALBUMOFTHEYEAR = 1,
    RATEYOURMUSIC = 2,
    BESTEVERALBUMS = 3,
    METACRITIC = 4

class Album:
    def __init__(self,name:str,artist,rank:int,rating:int,website:Website=Website.UNDEFINED):
        self.website = website
        self.album = name
        self.artist = artist
        self.rank = rank
        self.rating = rating
    def __str__(self) -> str:
        return self.album+" by "+self.artist+" : "+str(self.rank)
    def __repr__(self) -> str:
        return self.album+" by "+self.artist+" : "+str(self.rank)
class Scraper:
    """Class to scrape a webpage, based on pages"""
    def __init__(self,website:Website,name:str,url,items_per_page,starting_page:int):
        self.name = name
        self.website = website
        self.url = url
        self.items_per_page = items_per_page

        self.starting_page = starting_page


    # interface definition
    def scrape_top_x(self,top_x,year,rescrape_old_data=False):
        """Scrape the top X albums of YYYY year"""
        # Scrape the page
        pass
    def scrape_page(self,year:int,page:int) -> str: # page starts at 0
        """Scrape the page of the website"""
        page_to_scrape = page + self.starting_page
        try:
            scraper = cloudscraper.create_scraper(
                interpreter="nodejs",
                delay=30,
                browser={
                    "browser": "chrome",
                    "platform": "ios",
                    "desktop": False,
                }
            )
            response = scraper.get(self.url.format(page=page_to_scrape,year=year))
            print(self.website.name+" : "+str(response.status_code))
            return response.text
        except Exception as e:
            print(e)
            return ''

    def parse_html(self,response:str) -> Optional[List[Album]]:
        pass
