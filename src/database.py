import asyncio
import logging
from functools import wraps
from pathlib import Path
from typing import List, Optional

from typing import Iterable, List, Optional

import aiosqlite
from aiosqlite import Row
from src.schema import SQL

def get_db_folder():
    """Gets the database folder, and creates one if it doesn't exist"""
    db_dir = Path.cwd() / "db"
    db_dir.mkdir(exist_ok=True)
    return db_dir

class Database:
    def __init__(self, db_name: str, db_folder: Path = get_db_folder()):
        """Initialise the SQLite Database. must include .sqlite file extension in Database name"""
        path = db_folder / db_name
        path.touch(exist_ok=True)
        self.db_path = path.resolve()
        self.db: Optional[aiosqlite.Connection] = None

    async def async_init(self):
        await self.connect()
        await self.initialise_database()

    async def connect(self):
        self.db = await aiosqlite.connect(self.db_path)

    async def execute(self, sql, values: tuple | List[tuple] | None, fetch: str = "none") -> Row | Iterable[Row] | None:
        if self.db is None or fetch not in ["none", "one", "all"]:
            return None
        async with self.db.cursor() as cursor:
            try:
                if values is None:
                    await cursor.execute(sql)
                elif isinstance(values, tuple):
                    await cursor.execute(sql, values)
                elif isinstance(values, list):
                    await cursor.executemany(sql, values)
                else:
                    raise ValueError("Invalid type for values parameter")
                result=None
                if fetch == "one":
                    result = await cursor.fetchone()
                elif fetch == "all":
                    result = await cursor.fetchall()
                else:
                    result = None

                await self.db.commit()
                return result
            except Exception as e:
                logging.error(f"Error executing SQL: {e}")
                await self.db.rollback()
                return None



    async def initialise_database(self):
        s1= await self.execute(SQL.create_albums_table,None)
        s2= await self.execute(SQL.create_spotify_table,None)
        s3 =await self.execute(SQL.create_text_to_spotify_table,None)
        return s1 and s2 and s3

    async def insert_album(self, website: str, year: int, rank: int, album: str, artist: str):
        return await self.execute(SQL.insert_album, (website, year, rank, album, artist))

    async def insert_spotify(self, spotify_id: str, album: str, artist: str, genres: str, release_date: str, image_url: str):
        return await self.execute(SQL.insert_spotify, (spotify_id, album, artist, genres, release_date, image_url))

    async def insert_text_to_spotify(self, album: str, artist: str, spotify_id: str):
        return await self.execute(SQL.insert_text_to_spotify, (album, artist, spotify_id))

    async def get_spotify(self, album: str, artist: str):
        ret = await self.execute(SQL.get_spotify, (album, artist), "one")
        if ret is None:
            logging.error(f"Spotify data not found for {album} by {artist}")
            ret = []
        return ret

    async def get_albums_range_top_x(self, start_year: int, end_year: int, top_rank: int):
        print(start_year, end_year, top_rank,type(start_year),type(end_year),type(top_rank))
        ret = await self.execute(SQL.get_albums_range_top_x, (start_year, end_year, top_rank), "all")
        if ret is None:
            logging.error(f"Data not found between {start_year} and {end_year} for top {top_rank} albums")
            ret = []
        return ret

    async def get_albums_aggregated(self, start_year: int, end_year: int):
        ret = await self.execute(SQL.get_albums_aggregated, (start_year, end_year), "all")
        if ret is None:
            logging.error(f"Aggregated Data not found between {start_year} and {end_year}")
            ret = []
        return ret







#
 #   async def insert_album(self,website, year, rank, title):
  #      return await self.execute(SQL.insert_album, (website, year, rank, title))

   # async def get_album(self,website, year, rank):
    #    return await self.execute(SQL.get_album, (website, year, rank),"one") # check order

    #async def get_all_albums(self):
     #   return await self.execute(SQL.get_all_albums, None,"many") # check order
