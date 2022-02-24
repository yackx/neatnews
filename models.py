from dataclasses import dataclass, field


@dataclass
class Headline:
    title: str
    category: str
    url: str
    internal_url: str
    paywall: bool | None


@dataclass
class Article:
    title: str
    summary: str
    img: str
    url: str
    paragraphs: [str]
    published_on: str = None
    updated_on: str = None
    see_also: [str] = field(default_factory=list)
