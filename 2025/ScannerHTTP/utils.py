import requests, csv, os, re
from bs4 import BeautifulSoup


url_pattern = "(https?://(?:www.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9].[^s]{2,}|www.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9].[^s]{2,}|https?://(?:www.|(?!www))[a-zA-Z0-9]+.[^s]{2,}|www.[a-zA-Z0-9]+.[^s]{2,})"


def fetch_data_from_site(site_url):
    """Fetch html code from the site in parameter, return site content

    :param site_url: URL of the site to catch
    :type site_url: string
    """

    r = requests.get(site_url)
    return r.text

def creating_soup(html_content):
    return BeautifulSoup(html_content, 'lxml')

def is_file_empty(file):
    return os.stat(f"./output/{file}").st_size == 0

def grab_all_links_from_existing_soup(soup, url_to_check, base_url):
    """Extract only links from soup and returning them in an array

    :param soup: Already existing soup (HTML code parsed with bs4)
    :type soup: string
    :param url_to_check: Current URL checked
    :type url_to_check: string
    :param base_url: Base url of the site, index page
    :type base_url: string
    """
    link_array = []
    links = soup.find_all('a')
    for link in links:
        if link.get("href"):
            #absolute URL
            if base_url in link.get("href"):
                link_array.append(link.get('href'))
            #relative URL
            if link.get("href")[0] == "/":
                link_array.append(base_url + link.get('href'))
    return list(set(link_array))

def output_text_to_file(link_to_write, file="output.csv"):
    """Write content to a CSV file

    :param link_to_write: URL to write
    :type content: str
    :param file: Name of the file
    :type file: str
    """

    with open(f"./output/{file}", 'a', newline='') as csvfile:
        fieldnames = ["URL", "Status_code"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if is_file_empty(file):
            writer.writeheader()
        writer.writerow({'URL':link_to_write, 'Status_code':requests.get(link_to_write).status_code})

def delete_content_of_file(file="output.csv"):
    with open(f"./output/{file}", "w", encoding='utf-8') as f:
        f.write('')

def is_valid_url(url):
    """Check an URL input, boolean return

    :param url: URL to check
    :type url: string
    """
    return True if re.match(url_pattern, url) else False

def extract_index_page(url):
    """http://www.google.com/contact --> http://www.google.com

    :param url: URL to extract main domain
    :type url: string
    """
    if "/" in url and "http" in url:
        return "http://" + url.split("/")[2]

def crawl_site(url, deepness=1):
    """Crawl the site recursively

    :param url: Beginning of the crawling way
    :type url: string
    :param deepness: Deepness of web crawling, defaults to 1
    :type deepness: int, optional
    """
    delete_content_of_file()
    soup = creating_soup(fetch_data_from_site(url))
    available_links = grab_all_links_from_existing_soup(soup, url)
    
    if deepness == 1:

        for link in list(set(available_links)):
            output_text_to_file(link)
    
    elif deepness == 2:

        for link in list(set(available_links)):
            soup = creating_soup(fetch_data_from_site(link))
            final_links = grab_all_links_from_existing_soup(soup, link)
            
            for final_link in list(set(final_links)):            
                output_text_to_file(final_link)

    else:
        print("Not a good idea to crawl so much...")

print(extract_index_page("http://www.google.com/contact"))