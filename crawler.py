import logging
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import json

"""
https://www.scrapingbee.com/blog/crawling-python/
"""

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)

class Crawler:

    def __init__(self, urls=[]):
        self.visited_urls = []
        self.urls_to_visit = urls
        self.numOfDownloadedURLs = 0
        self.webPages_data = [None for _ in range(2501)]

    def download_url(self, url):
        try:
            plain_text = requests.get(url).text
            soup = BeautifulSoup(plain_text, "html.parser")
            if( soup.title != None):
                appendix = ({
                    'url': url,
                    'title': soup.title.string,
                    'body': soup.get_text()
                })
            else:
                return ""
        except:
            return ""

        self.webPages_data[self.numOfDownloadedURLs] = appendix
        self.numOfDownloadedURLs += 1
        return plain_text

    def get_linked_urls(self, url, html):
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            path = link.get('href')
            if path and path.startswith('/'):
                path = urljoin(url, path)
                #print("path: ", path)
            yield path

    def add_url_to_visit(self, url):
        if url not in self.visited_urls and url not in self.urls_to_visit and url != None and \
                (url.__contains__("tr") or url.__contains__("turkce") or url.__contains__("turkey")) and not url.__contains__(".pdf") and not url.__contains__(".zip") and not url.__contains__(".rar") and not url.__contains__(".wav") and not url.__contains__(".mpg"):
            self.urls_to_visit.append(url)

    def crawl(self, url):
        html = self.download_url(url)
        for url in self.get_linked_urls(url, html):
            self.add_url_to_visit(url)

    def run(self):
        while self.urls_to_visit and self.numOfDownloadedURLs <= 2500:
            #print("self.urls_to_visit: ", self.urls_to_visit)
            logging.info(f'numOfDownloadedURLs: {self.numOfDownloadedURLs}')
            url = self.urls_to_visit.pop(0)
            logging.info(f'Crawling: {url}')
            try:
                self.crawl(url)
            except Exception:
                logging.exception(f'Failed to crawl: {url}')
            finally:
                self.visited_urls.append(url)

        with open("webPages2.json", "r", encoding="utf-8") as file:
            try:
                temp = json.load(file)
            except:
                temp = []

        for i in range(0, len(self.webPages_data)):
            if(self.webPages_data[i] != None):
                temp.append(self.webPages_data[i])

        with open("webPages2.json", "w", encoding="utf-8") as file:
            json.dump(temp, file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    Crawler(urls=['https://tr.wikipedia.org/wiki/Koronavirüs']).run()
    Crawler(urls=['https://covid19.saglik.gov.tr/']).run()
    Crawler(urls=['https://www.bbc.com/turkce/topics/ck0r47pk362t']).run()
    Crawler(urls=['https://www.acibadem.com.tr/koronavirus/koronavirus-corona-virusu-nedir-belirtileri/']).run()
