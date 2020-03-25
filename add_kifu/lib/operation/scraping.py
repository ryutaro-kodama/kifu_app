from bs4 import BeautifulSoup
import requests

class Scraping():
    def __init__(self, url):
        self.url = url

    def scrape(self):
        html = requests.get(self.url)
        soup = BeautifulSoup(html.text, "html.parser")
        text = soup.__str__()
        return text