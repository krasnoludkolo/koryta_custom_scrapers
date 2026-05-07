from bs4 import BeautifulSoup
from curl_cffi import requests as r


# TODO
# all cities
# all pages loop
# integrate to check when to stop

def get_from_city(city: str, page: int) -> list[str]:
    url = f"https://{city}.naszemiasto.pl/wiadomosci/{page}"
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'en-GB,en;q=0.8',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Not:A-Brand";v="99", "Brave";v="145", "Chromium";v="145"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'sec-gpc': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
    }

    response = r.get(url, headers=headers, impersonate='chrome')
    pass
    soup = BeautifulSoup(response.text, 'html.parser')
    articles_section = soup.find('section', attrs={'data-ea': 'articles_left'})

    all_urls = articles_section.find_all('a', attrs={'data-ec': "atomsListingArticleTileWithSeparatedLink"})
    all_urls = [article['href'] for article in all_urls if 'href' in article.attrs and article['href'].startswith('/')]

    return list(set(all_urls))  # remove duplicates


if __name__ == '__main__':
    get_from_city('poznan', 1)
