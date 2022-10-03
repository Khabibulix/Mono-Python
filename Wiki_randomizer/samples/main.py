import requests
from bs4 import BeautifulSoup
import webbrowser

if __name__ == "__main__":
    while True:
        r = requests.get("https://en.wikipedia.org/wiki/Special:Random")
        soup = BeautifulSoup(r.content, "html.parser")
        title = soup.find(class_="firstHeading").text
        print(f"{title} \nDo you want to view it? (Y/N)")
        answer = input("").lower()
        if answer == "y":
            url = "https://en.wikipedia.org/wiki/%s" % title
            webbrowser.open(url)
            break
        elif answer == "n":
            print("Try again!")
            continue
        else:
            print("Wrong choice!")
            break