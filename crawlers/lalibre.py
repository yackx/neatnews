import re

import requests
from bs4 import BeautifulSoup

from crawlers import google_bot_user_agent_header
from crawlers.crawler import Crawler
from models import Headline, Article


class LaLibre(Crawler):
    @staticmethod
    def code() -> str:
        return "lalibre"

    @staticmethod
    def name() -> str:
        return "La Libre"

    @staticmethod
    def base_url() -> str:
        return "https://lalibre.be"

    def fetch_headlines(self) -> [Headline]:
        headlines = []
        html = requests.get(self.base_url(), headers=google_bot_user_agent_header()).text
        soup = BeautifulSoup(html, "html.parser")

        for story_item_html in soup.select(".ap-StoryList-itemLink"):
            try:
                title = story_item_html.select("h2")[0].text
                if category_html := story_item_html.select(".ap-StoryListTags-item"):
                    category = category_html[0].text
                else:
                    category = "Divers"
                href = story_item_html.attrs["href"]
                url = self.base_url() + href
                internal_url = f"lalibre{href}"
                headline = Headline(title=title, category=category, url=url, internal_url=internal_url, paywall=False)
                headlines.append(headline)
            except IndexError:
                continue

        return list(dict.fromkeys(headlines))

    def fetch_article(self, path: str) -> Article:
        url = self.base_url() + "/" + path
        html = requests.get(url, headers=google_bot_user_agent_header()).text
        soup = BeautifulSoup(html, "html.parser")
        ap_story = soup.select(".ap-Story")[0]
        title = ap_story.find("h1").text

        try:
            summary = ap_story.find("h2").text
        except AttributeError:
            summary = None

        try:
            images = [i.attrs["src"] for i in ap_story.select("img")]
            images = [i for i in images if not i.startswith("data:image")]
            img = images[-1]
        except (AttributeError, IndexError):
            img = None

        paragraphs = []
        content_html = soup.select("#article-text")[0]
        for p in content_html.find_all("p"):
            content = p.text.strip().strip("\n")
            if content:
                paragraphs.append(p.text)

        return Article(title=title, summary=summary, img=img, url=url, paragraphs=paragraphs)
