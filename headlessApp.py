import src.database as DB
import src.scraping.albumoftheyear as AOTY
import asyncio
async def main():
    db = DB.Database("test.sqlite")
    await db.async_init()
    aoty = AOTY.AlbumOfTheYear()
    page = aoty.scrape_page(2023,0)
    print(page)
    content = aoty.parse_html(page)
    for c in content:
        print(c)




if __name__ == '__main__':
    m = asyncio.get_event_loop()
    m.run_until_complete(main())
    m.close()
