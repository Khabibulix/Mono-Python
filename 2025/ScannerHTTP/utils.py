import requests, csv, os, re, time


url_pattern = "(https?://(?:www.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9].[^s]{2,}|www.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9].[^s]{2,}|https?://(?:www.|(?!www))[a-zA-Z0-9]+.[^s]{2,}|www.[a-zA-Z0-9]+.[^s]{2,})"



def is_file_empty(file):
    return os.stat(f"./output/{file}").st_size == 0

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

def extract_domain_name(url):
    """http://www.google.com/contact --> google.com

    :param url: URL to extract domain name
    :type url: string
    """
    if "/" in url and "http" in url:
        return url.split("www.")[1]


def is_line_already_existing_in_file(line, file="output.csv"):
    with open(f"./output/{file}", "r", encoding='utf-8') as f:
        if line in f.read():
            return True
        return False
