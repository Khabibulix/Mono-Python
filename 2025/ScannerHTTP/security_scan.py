import requests, socket, json
from wappalyzer import analyze
from utils import extract_domain_name

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


def fetch_geolocation_for_ip(url):
    """Returns geographical infos about URL

    :param url: URL to analyze
    :type url: string, valid URL
    """
    ip_address = socket.gethostbyname(url)
    return requests.get(f'http://ip-api.com/json/{ip_address}').json()

def export_full_scan_to_json(url, file="scan.json"):
    """Generate full random into JSON file

    :param url: URL to scan
    :type url: string
    :param file: Name of JSON file, defaults to "scan.json"
    :type file: str, optional
    """
    ip = fetch_geolocation_for_ip(extract_domain_name(url))
    wapp = scan_with_wappalyzer(url)
    headers = scan_http_headers_with_requests(url)    
    with open(f"./output/{file}", 'w', newline='') as jsonfile:
        jsonfile.write(json.dumps({**wapp, **headers, **ip}, indent=4))

export_full_scan_to_json("http://www.jenesuis.net")