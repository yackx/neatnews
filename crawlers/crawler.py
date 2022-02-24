from abc import ABC, abstractmethod

from models import Headline, Article


class Crawler(ABC):
    @abstractmethod
    def code(self):
        pass

    @abstractmethod
    def fetch_headlines(self) -> [Headline]:
        pass

    @abstractmethod
    def fetch_article(self, path: str) -> Article:
        pass
