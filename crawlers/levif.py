import requests
from bs4 import BeautifulSoup

from crawlers import google_bot_user_agent_header
from crawlers.crawler import Crawler
from models import Headline, Article


class LeVif(Crawler):
    @staticmethod
    def code() -> str:
        return "levif"

    @staticmethod
    def name() -> str:
        return "Le Vif"

    @staticmethod
    def base_url() -> str:
        return "https://www.levif.be/"

    def fetch_headlines(self) -> [Headline]:
        headlines = []
        html = requests.get(self.base_url(), headers=google_bot_user_agent_header()).text
        soup = BeautifulSoup(html, "html.parser")

        for article_html in soup.select("article"):
            try:
                a = article_html.select("a")[1]
                title = a.text.strip()
                category = "News"
                href = a.attrs["href"].replace("//www.levif.be/", "")
                url = self.base_url() + href
                internal_url = f"{self.code()}/{href}"
                paywall = article_html.select(".m-plus")
                headline = Headline(title=title, category=category, url=url, internal_url=internal_url, paywall=paywall)
                headlines.append(headline)
            except IndexError:
                continue

        return headlines

    def fetch_article(self, path: str) -> Article:
        url = self.base_url() + "/" + path
        html = requests.get(url, headers=google_bot_user_agent_header()).text
        soup = BeautifulSoup(html, "html.parser")
        article_html = soup.select("article")[0]
        title = article_html.find("h1").text
        summary = article_html.select(".rmgDetail-intro")[0].text

        try:
            img_fragments = article_html.find_all("img")
            img_fragment = next(i for i in img_fragments if "itemprop" not in i.attrs)
            img = img_fragment.attrs["src"]
        except AttributeError:
            img = None

        paragraphs = []
        content_html = soup.select(".article-body")[0]
        for p in content_html.find_all("p"):
            content = p.text.strip().strip("\n")
            if content:
                paragraphs.append(p.text)

        return Article(title=title, summary=summary, img=img, url=url, paragraphs=paragraphs)
