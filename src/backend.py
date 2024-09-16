from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Annotated, Union

from fastapi import FastAPI, Header, Request
from uuid import uuid4

from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")






class ListItem:
    def __init__(self, text: str):
        self.id = uuid4()
        self.text = text
        self.done = False

list = [ListItem("test"), ListItem("test2"), ListItem("test3")]


@app.get("/list", response_class=HTMLResponse)
async def list_items(request: Request, hx_request: Annotated[Union[str, None], Header()] = None):
    if hx_request:
        return templates.TemplateResponse(
            request=request, name="list.html", context={"list": list}
        )
    return JSONResponse(content=jsonable_encoder(list))
