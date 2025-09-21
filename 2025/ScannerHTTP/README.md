# Scanner HTTP

### What i learned

I learned about Requests, BeautifulSoup, parsing, string methods

### How to launch

You can launch main.py using ```python main.py```, the other files will not display anything.

## The project

Originally the plan was to crawl automatically a website, for example, the app would seek links, visit them and display the content in a log file named _output.txt_.

BUT, now we want to display some security headers like server versions, known CVE, etc... A bit like Wappalyzer.

## Expectations at 21/09/25

- Asynchronous and fast crawling
- Anti-bot measures escaping
- Logging of status codes of all the internal links
- Identifying technologies for the site
- We want just a ```main.py http://www.google.com 3``` where _3_ will be the _deepness_ of the crawl and _http://www.google.com_ will be the URL to crawl.
