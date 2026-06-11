from scrapers.common import create_url_client
from scrapers.onet_scraper import OnetScraper
from scrapers.wp_scraper import WpScraper


def main():
    source = 'custom_scraper'

    wp_scraper = WpScraper(create_url_client(source))
    onet_scraper = OnetScraper(create_url_client(source))

    wp_scraper.collect_urls()
    onet_scraper.collect_urls()


if __name__ == '__main__':
    main()