import json

import requests
from bs4 import BeautifulSoup

from crawlers import google_bot_user_agent_header
from crawlers.crawler import Crawler
from models import Headline, Article


class Rtbf(Crawler):
    @staticmethod
    def code() -> str:
        return "rtbf"

    @staticmethod
    def name() -> str:
        return "rtbf"

    @staticmethod
    def base_url() -> str:
        return "https://www.rtbf.be"

    def fetch_headlines(self) -> [Headline]:
        headlines = []
        html = requests.get(self.base_url(), headers=google_bot_user_agent_header()).text
        soup = BeautifulSoup(html, "html.parser")

        raw_data = soup.find(id="__NEXT_DATA__")
        json_data = json.loads(raw_data.text)
        for i in json_data["props"]["pageProps"]["widgets"]:
            try:
                for j in i["props"]["articles"]:
                    category = j.get("category")
                    if not category:
                        category = "Divers"
                    href = f'/article/{j["href"]["query"]["pid"]}'
                    url = f'{self.base_url()}{href}'
                    internal_url = f'{self.code()}{href}'
                    headline = Headline(title=j["title"], category=category, url=url, internal_url=internal_url,
                                        paywall=False)
                    if headline not in headlines:
                        headlines.append(headline)
            except KeyError:
                pass

        return headlines

    def fetch_article(self, path: str) -> Article:
        url = self.base_url() + "/" + path
        html = requests.get(url, headers=google_bot_user_agent_header()).text
        soup = BeautifulSoup(html, "html.parser")

        article_html = soup.find(id="id-text2speech-article")
        title = article_html.find("h1").text
        summary = ""
        try:
            img = article_html.find("img").attrs["src"]
        except AttributeError:
            img = None

        paragraphs = []
        content_html = article_html.find(id="content")
        for p in content_html.find_all("p"):
            content = p.text.strip().strip("\n")
            if content:
                paragraphs.append(p.text)

        return Article(title=title, summary=summary, img=img, url=url, paragraphs=paragraphs)
