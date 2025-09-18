# Display a webpage and its titles
# Display all links in page and titles including the name of the link

from utils import creating_soup, fetch_data_from_site, grab_all_links_from_existing_soup

url = "http://jenesuis.net/"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def main():
    site_content = fetch_data_from_site(url)
    soup = creating_soup(site_content)
    print(grab_all_links_from_existing_soup(soup))

if __name__ == "__main__":
    main()