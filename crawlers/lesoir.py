import re

import requests
from bs4 import BeautifulSoup
from bs4.element import Comment

from models import Headline, Article

base_url = "https://lesoir.be"


def fetch_headlines() -> [Headline]:

    def parse_panel_fragment(selector):
        articles_in_panel = []
        for article_fragment in panel_fragment.select(selector):
            title = article_fragment.text.strip().replace("\n", " - ")
            href = article_fragment.attrs["href"]
            internal_url = f"lesoir{href}"
            url = f"{base_url}{href}"
            paywall = len(article_fragment.select(".r-icon--lesoir")) > 0
            article = Headline(title, str(category), url, internal_url, paywall)
            articles_in_panel.append(article)
        return articles_in_panel

    articles = []
    html = requests.get(base_url).text
    soup = BeautifulSoup(html, "html.parser")
    category = None

    for panel_fragment in soup.find_all("r-main", id=re.compile("^main")):
        category = "A la Une"
        articles_in_link_fragment = parse_panel_fragment(".r-article--link")
        articles.extend(articles_in_link_fragment)

    for panel_fragment in soup.find_all("r-mini-panel", id=re.compile("^panel")):
        try:
            category = panel_fragment.select(".r-mini-panel--title")[0].attrs["data-label"]
            print(f"    {category}")
            articles_in_link_fragment = parse_panel_fragment(".r-article--link")
            if len(articles_in_link_fragment) == 0:  # Panel "Opinions"
                articles_in_link_fragment = parse_panel_fragment(".r-panel--link")
            articles.extend(articles_in_link_fragment)
        except IndexError:
            pass

    # Dedup articles in "A la Une" category - this category is flooded with duplicates
    for i, article in enumerate([a for a in articles if a.category == "A la Une"]):
        if i > 5:  # Make sure important articles appear even if duped
            try:
                next(a for a in articles if a.url == article.url and a.category != "A la Une")
                articles.remove(article)
            except StopIteration:
                pass

    return articles


def fetch_article(path: str) -> Article:
    url = base_url + "/" + path
    html = requests.get(url, headers={"user-agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"}).text
    soup = BeautifulSoup(html, "html.parser")
    title = soup.select("h1")[0].text
    summary = soup.select("r-article--chapo p")[0].text

    paragraphs = []

    try:
        content_html = soup.select("article")[0]

    except IndexError:
        content_html = soup.select("r-article--section")[0]

    img_src = content_html.find("figure").find("img").attrs["src"]
    img = base_url + img_src

    for p in content_html.find_all("p"):
        # try:
        #     twitter = soup.select(".twitter-tweet")[0]  # .select("a")[0].text
        #     paragraphs.append(f"Twitter: {twitter}")
        # except IndexError:
        #     pass

        if not any(type(e) == Comment and str(e).strip().startswith("scald") for e in p.descendants):
            # if not any(e for e in content_html.find_all("p")[15].descendants if type(e) == Comment):
            content = p.text.strip().strip("\n")
            if content:
                paragraphs.append(p.text)

    return Article(title=title, summary=summary, img=img, url=url, paragraphs=paragraphs)
