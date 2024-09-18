from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Annotated, Union

from fastapi import FastAPI, Header, Request
from uuid import uuid4

from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

import asyncio


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

        self.app = Application(db, aoty, bea, rym, meta, spotify)
        self.db_name = db

        self.fast = fast
        cwd = Path.cwd()
        fast.mount("/static",
            StaticFiles(directory=cwd / "static"),
            name="static",
        )
        self.templates = Jinja2Templates(directory="templates")
        self.list = [self.ListItem("test"), self.ListItem("test2"), self.ListItem("test3")]
        self.setup_routes()


    def setup_routes(self):
        self.fast.add_api_route("/", self.index, methods=["GET"], response_class=HTMLResponse)
        self.fast.add_api_route("/list", self.list_items, methods=["GET"], response_class=HTMLResponse)


    async def index(self, request: Request):
        return self.templates.TemplateResponse("index.html", {"request": request})

    async def list_items(self, request: Request, hx_request: Annotated[Union[str, None], Header()] = None):
        if hx_request:
            return self.templates.TemplateResponse(
                "list.html", {"request": request, "list": self.list}
            )
        return JSONResponse(content=jsonable_encoder(self.list))




    class ListItem:
        def __init__(self, text: str):
            self.id = uuid4()
            self.text = text
            self.done = False

#backend = Backend()
#backend = asyncio.run(backend.startup())
