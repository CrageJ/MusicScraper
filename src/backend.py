from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Annotated, Union

from fastapi import FastAPI, Header, Request
from uuid import uuid4

import logging

from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response

import asyncio
from collections import defaultdict


from fastapi import FastAPI, Request, Header
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from uuid import uuid4
from typing import Union, Annotated
from fastapi.encoders import jsonable_encoder
from pathlib import Path

from src.application import Application

class Backend:
    """Handles website serving, serving data, and handling requests."""
    def __init__(self, fast: FastAPI,
        db = '',
        aoty = False,
        bea = False,
        rym = False,
        meta = False,
        spotify = False):

        self.is_aoty = aoty
        self.is_bea = bea
        self.is_rym = rym
        self.is_meta = meta
        self.is_spotify = spotify

        self.app = Application(db)
        self.db_name = db

        self.fast = fast
        cwd = Path.cwd()
        fast.mount("/static",
            StaticFiles(directory=cwd / "static"),
            name="static",
        )
        self.templates = Jinja2Templates(directory="templates")

        self.setup_routes()

    async def async_init(self):
        await self.app.async_init()


    def setup_routes(self):
        self.fast.add_api_route("/", self.index, methods=["GET"], response_class=HTMLResponse)
        self.fast.add_api_route("/scrape", self.scrape, methods=["GET"], response_class=HTMLResponse)
        self.fast.add_api_route("/get", self.get_list, methods=["GET"], response_class=HTMLResponse)



    async def index(self, request: Request):
        return self.templates.TemplateResponse("index.html", {"request": request})

    async def scrape(self, request: Request):
        params = request.query_params
        rym = params.get("rym") == "on"
        aoty = params.get("aoty") == "on"
        bea = params.get("bea") == "on"
        meta = params.get("meta") == "on"
        from_year = int(params.get("from-year", 0))
        to_year = int(params.get("to-year", 0))
        top_x = int(params.get("top-x", 0))
        print(rym, aoty, bea, meta, from_year, to_year, top_x)

        # Process the data (you'll need to implement this part)
        # For example:
        await self.app.scrape_websites(top_x,from_year, to_year,aoty, bea,rym, meta)

        # Return the result
        return "[Scraped data successfully!]"

    async def get_list(self, request: Request):
        params = request.query_params
        rym = params.get("rym") == "on"
        aoty = params.get("aoty") == "on"
        bea = params.get("bea") == "on"
        meta = params.get("meta") == "on"
        from_year = int(params.get("from-year", 0))
        to_year = int(params.get("to-year", 0))
        top_x = int(params.get("top-x", 0))
        print(rym, aoty, bea, meta, from_year, to_year, top_x)

        con = await self.app.get_content(top_x,from_year, to_year,aoty, bea,rym, meta)
        groups = defaultdict(list)
        class display_element:
            def __init__(self, album_data):
                self.website = album_data["website"]
                self.year = album_data["year"]
                self.rank = album_data["rank"]
                self.title = album_data["album"]
                self.artists_str = album_data["artist"]
                self.image = album_data["img_url"]
                self.url = ''
                # Spotify data
                if album_data["spotify"]:
                    spotify_data = album_data["spotify"]
                    self.spotify_id = spotify_data["id"]
                    self.spotify_album = spotify_data["album"]
                    self.spotify_artist = spotify_data["artist"]
                    self.genres = spotify_data["genres"]
                    self.release_date = spotify_data["release_date"]
                    self.spotify_image_url = spotify_data["image_url"]
                    self.url = f"https://open.spotify.com/album/{self.spotify_id}"
                else:
                    self.spotify_id = None
                    self.spotify_album = None
                    self.spotify_artist = None
                    self.genres = None
                    self.release_date = None
                    self.spotify_image_url = None



        for element in con:
            el = display_element(element)
            groups[el.website].append(el)
        rendered_lists = []
        for website, albums in groups.items():
            rendered_list = self.templates.TemplateResponse(
                "albumlist.html",
                {"request": request, "albums": albums, "website": website}
            )
            rendered_lists.append(rendered_list.body.decode())

        # Combine all rendered lists into a single response
        combined_response = "<div>" + "</div><div>".join(rendered_lists) + "</div>"

        return HTMLResponse(content=combined_response)












#backend = Backend()
#backend = asyncio.run(backend.startup())
