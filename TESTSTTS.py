import src.scraping.besteveralbums as BEA
import src.scraping.albumoftheyear as AOTY
import src.scraping.rateyourmusic as RYM
import src.scraping.metacritic as META
import io
import asyncio

async def main():

    bea = BEA.BestEverAlbums()
    meta = META.MetaCritic()


    b = bea.scrape_page(2010, 0)
    m = meta.scrape_page(2010, 0)
    with open("TESTSCRAPE", "w") as f:
        f.write(">>>>>>>>>BEA>>>>>>>>>")
        f.write(b)
        f.write(">>>>>>>>META>>>>>>>>>")
        f.write(m)

if __name__ == "__main__":
    asyncio.run(main())
