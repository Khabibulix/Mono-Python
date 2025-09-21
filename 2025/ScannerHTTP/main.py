import random
from utils import *

# url_list = ["http://jenesuis.net", "https://www.data-bird.co/blog/web-scraping-python", "https://repo.zenk-security.com/"]
# url = random.choice(url_list)
url = "http://jenesuis.net"
html = '''<a href="/test"></a>
<a href="http://jenesuis.net/test"></a>
Prout
<a href="/test2"></a>
<a href="http://jenesuis.net/wallah"></a>"'''
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def main():
    soup_test = creating_soup(html)
    print(grab_all_links_from_existing_soup(soup_test, url))
    # delete_content_of_file("output.txt")
    # soup =  creating_soup(fetch_data_from_site(url))
    # crawl_site(url)
    
    # while True:
    #     available_links = grab_all_links_from_existing_soup(soup, url)
        
    #     for link in available_links:
    #         print(f"{available_links.index(link)}:  {link}\n")

    #     index_of_site = input("Choose the number of the link:  ")
    #     new_url = available_links[int(index_of_site)]
    #     soup = creating_soup(fetch_data_from_site(new_url))
    #     crawl_site(new_url)



if __name__ == "__main__":
    main()