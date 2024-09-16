
from typing import List
from enum import Enum

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
    def __init__(self,website:Website,album_name:str,artist:str,rank:int):
        self.website = website
        self.album_name = album_name
        self.artist = artist
        self.rank = rank



class Scraper:
    """Class to scrape a webpage, based on pages"""
    def __init__(self,db,website:Website,url,items_per_page,starting_page=1):
        self.db = db
        self.website = website
        self.url = url
        self.items_per_page = items_per_page

        self.starting_page = starting_page


    # interface definition
    def scrape_top_x(self,top_x,year,rescrape_old_data=False):
        """Scrape the top X albums of YYYY year"""
        # Scrape the page
        pass

    def get_data(self,top_x,year,scrape_if_missing=False):
        """Get the top X albums of YYYY year"""
        # Get the data from db

        # If some top_x data is missing and scrape_if_missing, scrape the page

        pass
