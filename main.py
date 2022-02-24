from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

from lesoir import fetch_headlines, Headline, fetch_article

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def split_headlines_in_categories(headlines: [Headline]) -> [str, [Headline]]:
    from collections import OrderedDict
    categories = list(OrderedDict.fromkeys([h.category for h in headlines]))
    split = []
    for category in categories:
        split.append((category, [h for h in headlines if h.category == category]))
    return split


def newspapers() -> {str, str}:
    return {"lesoir": "Le Soir"}


@app.get("/{newspaper}", response_class=HTMLResponse, name="newspaper")
async def headlines(request: Request):
    headlines = fetch_headlines()
    headlines_in_categories = split_headlines_in_categories(headlines)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "headlines_in_categories": headlines_in_categories,
        "newspapers": newspapers(),
    })


@app.get("/{newspaper}/{path:path}", response_class=HTMLResponse)
async def article(request: Request, path: str):
    article = fetch_article(path)
    return templates.TemplateResponse("article.html", {
        "request": request,
        "article": article,
        "newspapers": newspapers(),
    })


@app.get("/")
async def root(request: Request):
    url = str(request.base_url) + "lesoir"
    response = RedirectResponse(url=url)
    return response
