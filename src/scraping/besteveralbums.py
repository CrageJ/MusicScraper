import scraper as s

class BestEverAlbums(s.Scraper):
    def __init__(self,db):
        super().__init__(db,
            s.Website.BESTEVERALBUMS,
            "https://www.besteveralbums.com/yearstats.php?y={year}&f=&fv=&orderby=InfoRankScore&sortdir=DESC&page={page}",
            10)
