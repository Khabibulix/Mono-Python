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

def grab_all_links_from_existing_soup(soup, base_url):
    """Extract only links from soup and returning them in an array

    :param soup: Already existing soup (HTML code parsed with bs4)
    :type soup: string
    :param base_url: Base url, first crawled
    :type base_url: string
    """
    link_array = []
    links = soup.find_all('a')
    for link in links:
        #absolute URL
        if base_url in link.get("href"):
            link_array.append(link.get('href'))
        #relative URL
        else:
            link_array.append(base_url + link.get('href'))
    return list(set(link_array))

def separate_internal_and_external_links(link_array, base_url):
    """Returns two arrays, one of external links and one of internal links

    :param link_array: String array of all availables links on the original page
    :type link_array: array
    :param base_url: Base url, first crawled
    :type base_url: string
    """
    ext_links = []
    int_links = []

    for link in link_array:
        if base_url in link:
            int_links.append(link)
        else:
            ext_links.append(link)

    return int_links, ext_links

def are_all_link_available(link_array, base_url):
    """Returning true if status code for all available links is OK

    :param link_array: String array of all availables links on the original page
    :type link_array: array
    :param base_url: Base url, first crawled
    :type base_url: string
    """
    status_code_array = []

    if len(link_array) == 0:
        return False

    for link in link_array:
        status_code = requests.get(link).status_code
        status_code_array.append(status_code == 200)
    
    if all(status_code_array):
        return True

def output_text_to_file(content, file):
    """Write content to a file

    :param content: Data to write
    :type content: str
    :param file: Name of the file
    :type file: str
    """
    with open(f"./output/{file}", "a", encoding="utf-8") as f:
        f.write(content)

def delete_content_of_file(file):
    with open(f"./output/{file}", "w", encoding='utf-8') as f:
        f.write('')

def clean_soup(soup):
    for data in soup(['style', 'script']):
        data.decompose()
    return ' '.join(soup.stripped_strings)

def crawl_site(url, deepness=1):
    """Crawl the site recursively

    :param url: Beginning of the crawling way
    :type url: string
    :param deepness: Deepness of web crawling, defaults to 1
    :type deepness: int, optional
    """
    soup =  creating_soup(fetch_data_from_site(url))
    
    output_text_to_file(f"{url} contains: \n {clean_soup(soup)}", "output.txt")
    
    # crawl_site(links.pop(), links)