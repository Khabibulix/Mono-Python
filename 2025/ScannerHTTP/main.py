import random, argparse
from utils import *

# url_list = ["http://jenesuis.net", "https://www.data-bird.co/blog/web-scraping-python", "https://repo.zenk-security.com/"]
# url = random.choice(url_list)
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def main(url, deepness):
    crawl_site(url, deepness)
    
    # while True:
    #     available_links = grab_all_links_from_existing_soup(soup, url)
        
    #     for counter, link in enumerate(available_links):
    #         print(f"{counter}:\t{link}\n")

    #     index_of_site = input("Choose the number of the link:  ")
    #     new_url = available_links[int(index_of_site)]
    #     soup = creating_soup(fetch_data_from_site(new_url))
    #     crawl_site(new_url)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script that crawls a website for security purposes")
    parser.add_argument("--url", required=True, type=str, help="URL of the site, base point to start crawling")
    parser.add_argument("--deepness", required=False, type=int, help="By default, is equal to 1, it represents how deep the crawler will go.")
    args = parser.parse_args()
    url = args.url
    deepness = args.deepness
    main(url, deepness)