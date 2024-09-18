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
class Backend:
    def __init__(self):
        self.app = FastAPI()
        self.templates = Jinja2Templates(directory="templates")
        self.list = [self.ListItem("test"), self.ListItem("test2"), self.ListItem("test3")]

    async def startup(self):
        @self.app.get("/", response_class=HTMLResponse)
        async def index(request: Request):
            return self.templates.TemplateResponse(request=request, name="index.html")

        @self.app.get("/list", response_class=HTMLResponse)
        async def list_items(request: Request, hx_request: Annotated[Union[str, None], Header()] = None):
            if hx_request:
                return self.templates.TemplateResponse(
                    request=request, name="list.html", context={"list": self.list}
                )
            return JSONResponse(content=jsonable_encoder(self.list))

    class ListItem:
        def __init__(self, text: str):
            self.id = uuid4()
            self.text = text
            self.done = False

backend = Backend()
backend = asyncio.run(backend.startup())
