import logging
import chromedriver_binary
import csv

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from operator import itemgetter
from selenium import webdriver

# HOOK_URL = 'https://hooks.slack.com/services/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'
# SLACK_CHANNEL = 'report-test'

def CoinTelegraph(channel):
    url = "https://cointelegraph.com/search?query=dao"
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    browser = webdriver.Chrome("./chromedriver_binary/chromedriver", options=options)
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

        except:
            pass

    history = articleHistory()
    newArticles = []

    for article in articles:
        if len(newArticles) == 3:
            break
        
        for his in history:
            if article[0] == his[0]:
                break
        else:
            print(article)
            newArticles.append(article)


    writeCSV(newArticles)
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

def articleHistory():
    history = []
    with open('./some.csv') as f:
        reader = csv.reader(f)
        for line in reader:
            history.append(line)

    return history


def writeCSV(history):
    with open('./some.csv', 'a') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(history) 
