from abc import ABC, abstractmethod

from models import Headline, Article


class Crawler(ABC):
    @staticmethod
    @abstractmethod
    def code() -> str:
        pass

    @staticmethod
    @abstractmethod
    def name() -> str:
        pass

    @staticmethod
    @abstractmethod
    def base_url() -> str:
        pass

    @abstractmethod
    def fetch_headlines(self) -> [Headline]:
        pass

    @abstractmethod
    def fetch_article(self, path: str) -> Article:
        pass


def crawler_by_code(code: str) -> Crawler | None:
    for crawler_class in Crawler.__subclasses__():
        if crawler_class.code() == code:
            return crawler_class()

    return None


def newspapers_by_code() -> {str: str}:
    return {c.code(): c.name() for c in Crawler.__subclasses__()}


def google_bot_user_agent_header() -> {str, str}:
    return {"user-agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"}
