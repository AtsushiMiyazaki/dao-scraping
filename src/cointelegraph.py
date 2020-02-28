import logging
import csv

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from operator import itemgetter
from selenium import webdriver
from filehandler import FetchFileFromS3, WriteFileToS3

CT_CSV='cointelegraph.csv'

def CoinTelegraph(channel):
    url = "https://cointelegraph.com/search?query=dao"
    options = webdriver.ChromeOptions()
    options.binary_location = "/opt/headless/lib/bin/headless-chromium"
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument("--single-process")
    options.add_argument('--disable-dev-shm-usage')

    browser = webdriver.Chrome(executable_path="./chromedriver_binary/chromedriver", options=options)
    browser.get(url)
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    rows = soup.find_all('div', class_='row result')

    articles = []

    for article in rows:
        try:
            link = article.a.get("href")
            title = article.h2.a.string
            articles.append((link, title))

        except Exception as e:
            logging.error(e)
            pass

    history = FetchFileFromS3(CT_CSV)
    newArticles = []

    for article in articles:
        if len(newArticles) == 3:
            break
        for his in history:
            if article[0] == his[0]:
                break
        else:
            newArticles.append(article)

    WriteFileToS3(newArticles + history, CT_CSV)

    message = f"""　
    ====================
      :postal_horn:  *CoinTelegraph* :postal_horn:
    ====================
    """

    if newArticles == []:
        print("new article is empty")
        message = message + f"""
            :sleeping: DAO関連記事の更新がありませんでした。
        """
    else:
        for i, new in enumerate(newArticles):
            if(i > 2):
                break
            message = message + f"""
                :eyes: DAO関連記事{i+1}
                *{new[1]}*
                {new[0]}
            """

    return {
        'channel': channel,
        'text': message
    }

# CoinTelegraph('report-test')