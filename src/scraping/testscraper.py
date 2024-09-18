import cloudscraper

scraper = cloudscraper.create_scraper(
    interpreter="nodejs",
    delay=10,
    browser={
        "browser": "chrome",
        "platform": "ios",
        "desktop": False,
    }
)

response = scraper.get("https://www.albumoftheyear.org/ratings/user-highest-rated/2021/1/")
print(response.status_code)
print(response.text)
