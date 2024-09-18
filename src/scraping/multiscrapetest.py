import albumoftheyear
import besteveralbums
import metacritic
import rateyourmusic
import time as t

def main():
    scrapers = [
        albumoftheyear.AlbumOfTheYear(None),
        besteveralbums.BestEverAlbums(None),
        metacritic.Metacritic(None),
        rateyourmusic.RateYourMusic(None)]
    n = len(scrapers)
    results = [None] * n
    prevtime =0
    for idx,scraper in enumerate(scrapers):
        start_time = t.time()
        results[idx] = scraper.scrape_page(2023,1)
        elapsed_time = t.time() - start_time
        wait_time = max(0,30-elapsed_time)
        t.sleep(wait_time)

    for scraper,result in zip(scrapers,results):
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print("%%%%%%%%%%%%%%"+scraper.name+"%%%%%%%%%%%%%%")
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print(result)
    return


if __name__ == "__main__":
    main()
