import scraper as s

class Metacritic(s.Scraper):
    def __init__(self,db):
        super().__init__(db,
            s.Website.METACRITIC,
            "https://www.metacritic.com/browse/albums/score/metascore/year/filtered?year_selected={year}&distribution=&sort=desc&view=detailed&page={page}",
            100,
            0)
