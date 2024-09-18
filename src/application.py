import src.scraping.albumoftheyear as AOTY
import src.scraping.besteveralbums as BEA
import src.scraping.rateyourmusic as RYM
import src.scraping.metacritic as META
import src.spotify as SPOTIFY
import src.database as DB

import logging


# handles all data processing, NOT website backend
class Application:
    def __init__(self,
        db = '',
        aoty = False,
        bea = False,
        rym = False,
        meta = False,
        spotify = False
    ):
        self.db = DB.Database(db) if db!='' else None
        self.aoty = AOTY.AlbumOfTheYear() if aoty else None
        self.bea = BEA.BestEverAlbums() if bea else None
        self.rym = RYM.RateYourMusic() if rym else None
        self.meta = META.MetaCritic() if meta else None
        self.spotify = SPOTIFY.Spotify() if spotify else None
        # Initialize logger
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        self.logger.info("Application Started")
