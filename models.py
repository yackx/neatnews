from dataclasses import dataclass, field
from typing import Union, Tuple


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
    paragraphs: [Union[str, Tuple[str, str]]]  # str=text, (str, str)=url,text
    published_on: str = None
    updated_on: str = None
    see_also: [str] = field(default_factory=list)
