import requests

def fetch_data(url, headers):

    r = requests.get(url, headers)

    with open("./output/output.txt", "w") as file:
        file.write(r.text)

