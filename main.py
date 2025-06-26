import json
import random
import os

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
QUOTES_PATH = os.path.join(BASE_DIR, "quotes.json")


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        with open(QUOTES_PATH, "r") as f:
            app.state.quotes = json.load(f)["quotes"]
            app.state.max_day = len(app.state.quotes)
    except Exception as e:
        print(f"Failed to load quotes.json: {e}")
        app.state.quotes = ["Default quote in case of error."]
        app.state.max_day = 1
    yield


app = FastAPI(lifespan=lifespan)
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
