import json
import random

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates



@asynccontextmanager
async def load_quotes(app: FastAPI):
    with open("quotes.json") as f:
        app.state.quotes = json.load(f)["quotes"]
        app.state.max_day = len(app.state.quotes)
    yield


app = FastAPI(lifespan=load_quotes)
templates = Jinja2Templates(directory="templates")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/quotes", response_class=HTMLResponse)
def get_quote(request: Request, fancy: bool = False, day: int = -1):
    quotes = app.state.quotes
    max_day = app.state.max_day

    quote = quotes[day - 1] if 0 < day <= max_day else random.choice(quotes)
    
    if fancy:
        return templates.TemplateResponse("quote.html", {"request": request, "quote": quote})
    return quote
