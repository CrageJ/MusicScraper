import asyncio
import logging
from functools import wraps
from pathlib import Path
from typing import List, Optional

import aiosqlite
from src.schema import SQL

def get_db_folder():
    """Gets the database folder, and creates one if it doesn't exist"""
    db_dir = Path.cwd() / "db"
    db_dir.mkdir(exist_ok=True)
    return db_dir


class Database:
    def __init__(self,db_name:str,db_folder:Path = get_db_folder()):
        """Initialise the SQLite Database. must include .sqlite file extension in Database name"""
        path = db_folder / db_name
        path.touch(exist_ok=True)
        self.db_path = path.resolve()
        self.db : Optional[aiosqlite.Connection] = None

    async def async_init(self):
        await self.connect()
        await self.initialise_database()

    async def connect(self):
        self.db = await aiosqlite.connect(self.db_path)

    async def execute(self,sql,values: tuple | List[tuple] | None,fetch:str = "none"):
        if self.db is None or fetch not in ["none","one","many"]:
            return
        async with self.db.cursor() as cursor:
            try:
                result = None
                if values is None:
                    await cursor.execute(sql)
                if type(values) == tuple:
                    await cursor.execute(sql,values)
                if type(values) == list:
                    await cursor.executemany(sql,values)

                if fetch == "one":
                    result = await cursor.fetchone()
                elif fetch == "all":
                    result = await cursor.fetchall()
                else:
                    result = True
                await self.db.commit()
                return result
            except Exception as e:
                logging.error(f"Error executing SQL: {e}")
                await self.db.rollback()
                return False



    async def initialise_database(self):
        await self.execute(SQL.create_albums_table,None)
        await self.execute(SQL.create_spotify_table,None)
        await self.execute(SQL.create_text_to_spotify_table,None)

    async def insert_album(self,website, year, rank, title):
        await self.execute(SQL.insert_album, (website, year, rank, title))

    async def get_album(self,website, year, rank):
        return await self.execute(SQL.get_album, (website, year, rank),"one") # check order

    async def get_all_albums(self):
        return await self.execute(SQL.get_all_albums, None,"many") # check order
