from bs4 import BeautifulSoup
from pip._vendor import requests


class Extractor(object):
    target_url = ""
    my_href = []
    total = 500

    def __init__(self, url):
        self.target_url = url

    def extract(self):
        r = requests.get(self.target_url)
        print(r.status_code)
        return r

    def bs4(self):
        r = requests.get(self.target_url)
        soup = BeautifulSoup(r.content, 'html.parser')
        return soup

    def extract_article(self, target):
        print("extracting from " + target)
        self.target_url = target
        soup = self.bs4()
        notice = soup.find_all("div", 'justify-content-center')[0].text
        h1 = soup.find("h1").text
        h2 = soup.find("h2").text
        img = soup.figure.find('img').attrs['src']

        return {"title": h1,
                "sub_title": h2,
                "body": notice,
                "author": "Pulzo",
                "lecture_time": 4,
                "img": img}

    def search_href(self):
        soup = self.bs4()
        my_hrefs = []
        for link in soup.find_all('a'):
            h = link.get('href')
            if h is not None and "PP" in h and "contenido-patrocinado" not in h:
                if not str(h).startswith("https"):
                    h = "https://www.pulzo.com" + h
                my_hrefs.append(h)
        return my_hrefs

    def search_href_recursive(self):
        print(self.target_url)
        hrefs = self.search_href()
        if len(set(hrefs)) == 1:
            return
        self.my_href.extend(hrefs)
        print(len(self.my_href))
        for h in hrefs:
            if len(self.my_href) > self.total:
                break
            self.target_url = h
            self.search_href_recursive()
