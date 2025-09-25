# Scanner HTTP

### What i learned

I learned about Requests, BeautifulSoup, arguments parsing, string methods.

## Difficulties encountered

- Differents bugs with relative/absolute URLS. My solution was to extract the main domain to crawl my links.

### How to launch

You can get help typing ```python main.py -h```

A standard way of launching will be ``` python main.py --url http://www.google.com --deepness 2 --output output.csv```

## The project

Originally the plan was to crawl automatically a website, for example, the app would seek links, visit them and display the content in a log file named _output.txt_ in the folder _output_

BUT, now we want to display some security headers like server versions, known CVE, etc... The output will be in a CSV file, still in the folder _output_.

## Expectations at 21/09/25

- Asynchronous and fast crawling
- Anti-bot measures escaping using custom headers
- Logging of status codes of all the internal links
- Identifying technologies for the site
- We want just a ```main.py http://www.google.com 3``` where _3_ will be the _deepness_ of the crawl and _http://www.google.com_ will be the URL to crawl.

## What each Python script contains

- _utils.py_ contains all the internal logic except the code responsible for connection
