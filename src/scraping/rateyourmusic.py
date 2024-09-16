import scraper as s

class RateYourMusic(s.Scraper):
    def __init__(self,db):
        super().__init__(db,
            s.Website.RATEYOURMUSIC,
            "https://rateyourmusic.com/charts/top/album/{year}/{page}/",
            40)
