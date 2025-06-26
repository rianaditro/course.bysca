import json
import random
import os

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates



@asynccontextmanager
async def load_quotes(app: FastAPI):
    BASE_DIR = os.path.dirname(__file__)
    with open(os.path.join(BASE_DIR, "quotes.json")) as f:
        app.state.quotes = json.load(f)["quotes"]
        app.state.max_day = len(app.state.quotes)
    yield


app = FastAPI(lifespan=load_quotes)
templates = Jinja2Templates(directory="templates")


@app.get("/")
def read_root():
    return {"Hello": "World"}

def get_quote(day: int = -1):
    quotes = app.state.quotes
    max_day = app.state.max_day

    quote = quotes[day - 1] if 0 < day <= max_day else random.choice(quotes)
    return quote

@app.get("/quote")
def get_plain_quote(day: int = -1):
    return get_quote(day)

@app.get("/fancy-quote", response_class=HTMLResponse)
def get_fancy_quote(request: Request, fancy: bool = False, day: int = -1):
    quote = get_quote(day)
    return templates.TemplateResponse("quote.html", {"request": request, "quote": quote})
