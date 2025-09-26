import requests, csv, time
from bs4 import BeautifulSoup

from utils import delete_content_of_file, is_line_already_existing_in_file, is_file_empty, extract_index_page

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

def output_link_infos_to_file(link_to_write, file="output.csv"):
    """Write content to a CSV file

    :param link_to_write: URL to write
    :type content: str
    :param file: Name of the file
    :type file: str
    """

    with open(f"./output/{file}", 'a', newline='') as csvfile:
        fieldnames = ["URL", "Status_code", "Time_for_fetching_in_seconds"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if is_file_empty(file):
            writer.writeheader()
        start = time.time()
        status_code = requests.get(link_to_write).status_code
        end = time.time()
        writer.writerow({
            'URL':link_to_write,
            'Status_code':status_code,
            'Time_for_fetching_in_seconds': round(end - start, 4)})


def crawl_site(url, deepness, output_file):
    """Crawl the site recursively

    :param url: Beginning of the crawling way
    :type url: string
    :param deepness: Deepness of web crawling, defaults to 1
    :type deepness: int, optional
    """
    delete_content_of_file(output_file)
    soup = creating_soup(fetch_data_from_site(url))
    available_links = grab_all_links_from_existing_soup(soup, extract_index_page(url))
    
    if deepness == 1:

        for link in list(set(available_links)):
            if not is_line_already_existing_in_file(link, output_file):
                output_link_infos_to_file(link, output_file)
    
    elif deepness == 2:

        for link in list(set(available_links)):
            soup = creating_soup(fetch_data_from_site(link))
            final_links = grab_all_links_from_existing_soup(soup, extract_index_page(url))
            
            for final_link in list(set(final_links)):   
                if not is_line_already_existing_in_file(link, output_file):         
                    output_link_infos_to_file(final_link, output_file)

    else:
        print("Not a good idea to crawl so much...")
