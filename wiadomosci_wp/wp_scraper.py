import json
import time
from dataclasses import dataclass

import requests as r
from bs4 import BeautifulSoup


@dataclass
class PolskaResponse:
    urls: list[str]


def get_url_from_article_div(article_div) -> str:
    a_tag = article_div.find('a', href=True)
    if a_tag:
        return a_tag['href']
    return ''


def get_articles_from_polska_page(page: int) -> PolskaResponse:
    print(f"Getting articles from page {page}")

    url = f'https://wiadomosci.wp.pl/polska-6750773603044864k/{page}'  # TODO check if category id is constant
    response = r.get(url=url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # <script type="application/ld+json">
    script_tag = soup.find('script', attrs={'type': 'application/ld+json'})

    json_loads = json.loads(script_tag.string)
    articles_object = None
    for item in json_loads['@graph']:
        if item['@type'] == 'CollectionPage':
            articles_object = item
            break
    if not articles_object:
        print(f"No articles found on page {page}")
        # TODO monitor it
        return PolskaResponse(urls=[])
    urls = [item['url'] for item in articles_object['mainEntity']['itemListElement']]

    print(f"Found {len(urls)} articles on page {page}")
    return PolskaResponse(
        urls=urls
    )


def collect_urls() -> list[str]:
    page = 1 # Starts from 1
    urls = []
    for _ in range(5):
        response = get_articles_from_polska_page(page)
        urls.extend(response.urls)
        # TODO check from urls database if we already have some of the urls, if yes - stop, if no - continue
        page += 1
        time.sleep(1)  # just in case
    return list(set(urls))  # remove duplicates


if __name__ == '__main__':
    collect_urls()
