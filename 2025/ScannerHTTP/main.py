import random
from utils import *

# url_list = ["http://jenesuis.net", "https://www.data-bird.co/blog/web-scraping-python", "https://repo.zenk-security.com/"]
# url = random.choice(url_list)
url = "http://jenesuis.net"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
soup =  creating_soup(fetch_data_from_site(url))


def main():
    available_links = grab_all_links_from_existing_soup(soup, url)
    crawl_site(url, available_links)

if __name__ == "__main__":
    main()