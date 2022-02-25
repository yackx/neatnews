"""
Quick experiment without running the server
"""

if __name__ == '__main__':
    from crawlers.levif import LeVif
    crawler = LeVif()
    headlines = crawler.fetch_headlines()
    for headline in headlines:
        print(f"{headline.title} [{headline.category}]")
    print(f"{len(headlines)} articles")
