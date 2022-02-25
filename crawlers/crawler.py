from abc import ABC, abstractmethod

from models import Headline, Article


class Crawler(ABC):
    @staticmethod
    @abstractmethod
    def code():
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
