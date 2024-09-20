
from src.utils import Website
from typing_extensions import List, Optional
import cloudscraper
from bs4 import BeautifulSoup
import io

from time import sleep,time
from typing import Optional
from dataclasses import dataclass
import logging

SCRAPE_DELAY = 10

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


class Album:
    def __init__(self,name:str,artist,rank:int,rating:int,website:Website):
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

    def scrape_top_x_between_years(self,top_x,from_year,to_year,rescrape_old_data=False):
        """Scrape the top X albums between years
        In the format [(year,[html_content,...]),...]
        """
        arr = []
        for year in range(from_year,to_year+1):
            item = (year,self.scrape_top_x(top_x,year,rescrape_old_data))
            arr.append(item)
        return arr

    def scrape_top_x(self,top_x,year,rescrape_old_data=False) -> List[str]:
        """Scrape the top X albums of YYYY year"""
        if top_x < 1:
            return []
        pages = ((top_x-1) // self.items_per_page) + 1
        arr = []
        for i in range(pages):
            now = time()
            item = ''
            # if already scraped and rescrape is False, then skip
            if True: ######################### PLEASE MODIFY
                page = self.scrape_page(year,i)
                item = page
                leftover = max(0,SCRAPE_DELAY- (time() - now) )
                sleep(leftover)
            arr.append(item)

        return arr
    def scrape_page(self,year:int,page:int) -> str: # page starts at 0
        """Scrape the page of the website"""
        page_to_scrape = page + self.starting_page
        try:
            scraper = cloudscraper.create_scraper(
                interpreter="nodejs",
                delay=SCRAPE_DELAY,
                browser={
                    "browser": "chrome",
                    "platform": "ios",
                    "desktop": False,
                }
            )
            response = scraper.get(self.url.format(page=page_to_scrape,year=year))
            if response.status_code != 200:
                raise Exception("Bad status code")
            else:
                return response.text
        except Exception as e:
            logging.error(f"Website {self.website} Year {year} Page {page} Scraper: "+str(e))
            return ''
