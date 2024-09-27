import src.database as DB
import src.schema as SQL
import asyncio
async def main():
    db = DB.Database('myapp')
    await db.async_init()
    res = await db.get_albums_range_top_x(2021,2024,10)
    print(res)
    teststr = get_albums_range_top_x = """
    SELECT
        a.website,
        a.year,
        a.rank,
        a.album,
        a.artist
    FROM
        albums a
    WHERE
        a.year >= ? AND a.year <= ? AND a.rank <= ?
    ORDER BY
        a.website, a.year, a.rank"""
    #res2 = await db.execute(teststr,(0,2030,10),'all')
   # print(res2)


if __name__ == "__main__":

    asyncio.run(main())
