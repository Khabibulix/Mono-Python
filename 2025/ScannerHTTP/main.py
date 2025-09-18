# Display a webpage and its titles
# Display all links in page and titles including the name of the link

from utils import *

url = "http://jenesuis.net/"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def main():
    site_content = fetch_data_from_site(url)
    soup = creating_soup(site_content)
    available_links = grab_all_links_from_existing_soup(soup, url)
    internal_links, external_links = separate_internal_and_external_links(available_links, url)
    print(internal_links)
    print(external_links)
    print(are_all_link_available(internal_links, url))
    print(are_all_link_available(external_links, url))


if __name__ == "__main__":
    main()