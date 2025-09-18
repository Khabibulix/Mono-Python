import requests
from bs4 import BeautifulSoup

def fetch_data_from_site(site_url):
    """Fetch html code from the site in parameter, return site content

    :param site_url: URL of the site to catch
    :type site_url: string
    """

    r = requests.get(site_url)
    return r.text

def creating_soup(html_content):
    return BeautifulSoup(html_content, 'lxml')

def grab_all_links_from_existing_soup(soup):
    """Extract only links from soup and returning them in an array

    :param soup: Already existing soup (HTML code parsed with bs4)
    :type soup: string
    """
    link_array = []
    links = soup.find_all('a')
    for link in links:
        link_array.append(link.get('href'))
    return link_array
    
