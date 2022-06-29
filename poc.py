"""
Quick experiment without running the server
"""

import requests

from crawlers import google_bot_user_agent_header

headers = {
    "Host": "www.lecho.be",
    "User-Agent": "Mozilla / 5.0(Macintosh; Intel Mac OS X 10.15; rv:97.0) Gecko/20100101 Firefox/97.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
}


def print_page(url: str):
    html = requests.get(url, headers=headers).text
    print(html)
    return html


def print_google(q_url: str):
    html = requests.get("https://google.com/search", params={"q": q_url}).text
    print(html)
    return html


def crawl():
    from crawlers.levif import LeVif
    crawler = LeVif()
    headlines = crawler.fetch_headlines()
    for headline in headlines:
        print(f"{headline.title} [{headline.category}]")
    print(f"{len(headlines)} articles")


if __name__ == '__main__':
    # print_page("https://www.lecho.be/dossiers/conflit-ukraine-russie/cyberguerre-la-belgique-en-premiere-ligne-face-a-la-menace-russe/10371441.html")
    # print_google("https://www.lecho.be/dossiers/conflit-ukraine-russie/cyberguerre-la-belgique-en-premiere-ligne-face-a-la-menace-russe/10371441.html")
    crawl()
