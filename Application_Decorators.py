import os
from datetime import datetime
from functools import wraps
import requests
from bs4 import BeautifulSoup
import re
from Decorator import logger

@logger
def parse_habr():
    KEYWORDS = ['дизайн', 'фото', 'web', 'python']
    URL = "https://habr.com/ru/articles/"

    response = requests.get(URL)
    soup = BeautifulSoup(response.content, "lxml")

    articles = soup.find_all("div", class_="article-snippet" )
    found_articles = []

    for article in articles:
        title_tag = article.find("h2", class_="tm-title tm-title_h2")
        title = title_tag.text.strip()

        link_tag = title_tag.find("a", class_="tm-title__link")
        link = 'https://habr.com' + link_tag.get('href')

        date_tag = article.find('time')
        date = date_tag.get('title')

        preview_tag = article.find('div', class_='article-formatted-body article-formatted-body article-formatted-body_version-2')
        preview_text = preview_tag.text.strip() if preview_tag else ""

        hubs_tag = article.find('div', class_='tm-publication-hubs')
        hubs_text = ""
        if hubs_tag:
            hub_links = hubs_tag.find_all('span', class_='tm-publication-hub__link-container')
            hubs_text = ' '.join([hub.text.strip() for hub in hub_links])

        full_text = (preview_text + ' ' + title + ' ' + hubs_text).lower()
        for keyword in KEYWORDS:
            pattern = re.compile(keyword, re.IGNORECASE)
            if pattern.search(full_text):
                result_string = f"{date}-{title}-{link}"
                print(result_string)
                found_articles.append(result_string)
                break
    return found_articles

parse_habr()