if __name__ == '__main__':
    from crawlers.lesoir import fetch_headlines
    articles = fetch_headlines()
    for article in articles:
        print(f"{article.title} [{article.category}]")
    print(f"{len(articles)} articles")
