import re

import requests
from bs4 import BeautifulSoup
from bs4.element import Comment

from crawlers import google_bot_user_agent_header
from crawlers.crawler import Crawler
from models import Headline, Article


class LeSoir(Crawler):
    @staticmethod
    def code() -> str:
        return "lesoir"

    @staticmethod
    def name() -> str:
        return "Le Soir"

    @staticmethod
    def base_url() -> str:
        return "https://lesoir.be"

    def fetch_headlines(self) -> [Headline]:

        def parse_panel_fragment(selector):
            ext_urls = ["sosoir.lesoir.be", "clubdusoir.lesoir.be", "geeko.lesoir.be"]
            articles_in_panel = []
            for article_fragment in panel_fragment.select(selector):
                href = article_fragment.attrs["href"]
                if any(url for url in ext_urls if url in href):
                    continue
                internal_url = f"lesoir{href}"
                url = f"{self.base_url()}{href}"
                title = article_fragment.text.strip().replace("\n", " - ")
                paywall = len(article_fragment.select(".r-icon--lesoir")) > 0
                article = Headline(title, str(category), url, internal_url, paywall)
                articles_in_panel.append(article)
            return articles_in_panel

        articles = []
        html = requests.get(self.base_url(), headers=google_bot_user_agent_header()).text
        soup = BeautifulSoup(html, "html.parser")
        category = None

        for panel_fragment in soup.find_all("r-main", id=re.compile("^main")):
            category = "A la Une"
            articles_in_link_fragment = parse_panel_fragment(".r-article--link")
            articles.extend(articles_in_link_fragment)

        for panel_fragment in soup.find_all("r-mini-panel", id=re.compile("^panel")):
            try:
                category = panel_fragment.select(".r-mini-panel--title")[0].attrs["data-label"]
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

    def fetch_article(self, path: str) -> Article:
        url = self.base_url() + "/" + path
        html = requests.get(url, headers=google_bot_user_agent_header()).text
        soup = BeautifulSoup(html, "html.parser")
        title = soup.select("h1")[0].text
        summary = soup.select("r-article--chapo p")[0].text

        paragraphs = []

        try:
            content_html = soup.select("article")[0]
        except IndexError:
            content_html = soup.select("r-article--section")[0]

        img_src = content_html.find("figure").find("img").attrs["src"]
        img = self.base_url() + img_src

        for p in content_html.find_all("p"):
            if twitter_select := p.select("script"):
                # bs4 with html.parser does not expose the content of `scripts`
                # so we resort to regex
                try:
                    t = re.search('"https://twitter.com/(.*?)"', twitter_select[0].text).group(0).strip('"')
                    paragraphs.append((t, "Twitter"))
                except AttributeError:
                    pass
            elif not any(type(e) == Comment and str(e).strip().startswith("scald") for e in p.descendants):
                content = p.text.strip().strip("\n")
                if content:
                    paragraphs.append(p.text)

        return Article(title=title, summary=summary, img=img, url=url, paragraphs=paragraphs)
