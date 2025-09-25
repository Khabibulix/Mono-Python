import random, argparse
from utils import *

# url_list = ["http://jenesuis.net", "https://www.data-bird.co/blog/web-scraping-python", "https://repo.zenk-security.com/"]
# url = random.choice(url_list)
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def main(url, deepness, output_file):
    if is_valid_url(url):
        crawl_site(url, deepness, output_file)
    else:
        print("Url is invalid, please enter check it before launching app: ")
        return



if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description="Script that crawls a website for security purposes")
    # parser.add_argument("--url", required=True, type=str, help="URL of the site, base point to start crawling")
    # parser.add_argument("--deepness", required=False, type=int, help="By default, is equal to 1, it represents how deep the crawler will go.")
    # parser.add_argument("--output", required=False, type=int, help="By default, is equal to output.csv in the output folder, must be a csv file")
    # args = parser.parse_args()
    # url = args.url
    # deepness = args.deepness
    # output_file = args.output
    # main(url, deepness, output)
    main("http://www.jenesuis.net", 2, "output.csv")