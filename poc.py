if __name__ == '__main__':
    from crawlers.lalibre import LaLibre
    crawler = LaLibre()
    headlines = crawler.fetch_headlines()
    for headline in headlines:
        print(f"{headline.title} [{headline.category}]")
    print(f"{len(headlines)} articles")
