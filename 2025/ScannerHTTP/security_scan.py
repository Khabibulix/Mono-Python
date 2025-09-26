import requests
from wappalyzer import analyze

def scan_with_wappalyzer(url):
    """Grab technologies infos using wappalyzer module

    :param url: Url to scan
    :type url: string
    """
    return analyze(
        url= url,
        scan_type='balanced',
        threads=3
    )

def scan_http_headers_with_requests(url):
    """Grab useful HTTP headers for security 

    :param url: Url to scan
    :type url: string
    """
    return requests.get(url).headers

print(scan_http_headers_with_requests("http://jenesuis.net"))