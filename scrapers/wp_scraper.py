import json
import logging
import time
from typing import List

import requests as r
from bs4 import BeautifulSoup

from scrapers.url.url_client import UrlClient


# TODO
# - add regional


class WpScraper:

    def __init__(self, url_client: UrlClient, max_pages: int = 5):
        self.url_client: UrlClient = url_client
        self.max_pages: int = max_pages

    def get_articles_from_polska_page(self, page: int) -> List[str]:
        logging.info(f"[WP] Getting articles from page {page}")

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
            logging.info(f"[WP] No articles found on page {page}")
            # TODO monitor it
            return []
        urls = [item['url'] for item in articles_object['mainEntity']['itemListElement']]

        logging.info(f"[WP] Found {len(urls)} articles on page {page}")
        return urls

    def collect_urls(self):
        page = 1  # Starts from page 1
        urls = []
        for _ in range(self.max_pages):
            response_urls = self.get_articles_from_polska_page(page)
            urls.extend(response_urls)
            some_url_exists = self.url_client.any_url_exists(response_urls)
            self.url_client.add_urls(response_urls)
            if not response_urls or some_url_exists:
                break
            page += 1
            time.sleep(1)  # just in case
