import re
import time
from dataclasses import dataclass

import requests as r
from bs4 import BeautifulSoup


@dataclass
class KrajResponse:
    urls: list[str]
    has_next_page: bool


def get_url_from_article_div(article_div) -> str:
    a_tag = article_div.find('a', href=True)
    if a_tag:
        return a_tag['href']
    return ''


def get_articles_from_kraj_page(page: int) -> KrajResponse:
    print(f"Getting articles from page {page}")
    url = 'https://wiadomosci.onet.pl/partials/category/9fb1bb7c-e547-448b-8a4d-d286d4dd2fd0'  # TODO check if category id is constant
    params = {
        'strona': page,
        'mobile': 'false',
        'nextAdIndex': 0,
        'adsNoBanner': 'true',  # super duper ad block
        'cursor': None,  # Doesn't need it?
    }
    response = r.get(url=url, params=params)
    soup = BeautifulSoup(response.text, 'html.parser')

    list_div = soup.find('div', attrs={'data-section': re.compile('list-feed-[0-9]')})
    articles_divs = list_div.findChildren('div', recursive=False)
    urls = [get_url_from_article_div(article_div) for article_div in articles_divs]
    print(f"Found {len(urls)} articles on page {page}")
    return KrajResponse(
        urls=urls,
        has_next_page=response.text.__contains__('Pokaż więcej artykułów')
    )


def collect_urls() -> list[str]:
    page = 0
    urls = []
    for _ in range(5):
        response = get_articles_from_kraj_page(page)
        urls.extend(response.urls)
        # TODO check from urls database if we already have some of the urls, if yes - stop, if no - continue
        if not response.has_next_page:
            break
        page += 1
        time.sleep(1)  # just in case
    return list(set(urls))  # remove duplicates


if __name__ == '__main__':
    collect_urls()
