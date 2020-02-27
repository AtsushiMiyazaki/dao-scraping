import logging

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from operator import itemgetter

HOOK_URL = 'https://hooks.slack.com/services/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'
SLACK_CHANNEL = 'report-test'

def cointelegraph():
    url = "https://cointelegraph.com/search?query=dao"
    html = urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')
    rows = soup.find_all('div', class_='row result')

    articles = []

    
