from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from operator import itemgetter

def CoinMarketCap(hookUrl, channel):
    
    url = "https://coinmarketcap.com/"
    html = urlopen(url)
    soup = BeautifulSoup(html, "html.parser")
    rows = soup.find_all('tr', class_="cmc-table-row")

    coins = []
    iost = ()

    for tag in rows:
        try:
            td = tag.findAll('td')
            rank = td[0].find('div').string
            coinName = td[1].find('a').get("title")
            marketCap = td[2].find('div').string
            price = td[3].find('a').string
            volatility = float(td[6].find('div').string.split('%')[0])
            coinInfo = (
                rank,
                coinName,
                marketCap,
                price,
                volatility
            )

            if coinName == 'IOST':
                iost = coinInfo

            coins.append(coinInfo)
        
        except Exception as e:
            print(e)
            pass

    coins = sorted(coins, key=itemgetter(4))

    message = f"""　
        ==========================
        :iost: 今日のIOST :iost:

        ==========================
            順位: {iost[0]}位
            市場規模: {iost[2]}
            対ドル価格: {iost[3]}
            前日比: {iost[4]}%
        ==========================
    
        :sparkling_heart:*今日のコインベスト3*:sparkling_heart:

        ==========================
            *1位: {coins[-1][1]}*
            
            順位: {coins[-1][0]}位
            市場規模: {coins[-1][2]}
            対ドル価格: {coins[-1][3]}
            前日比: {coins[-1][4]}%
        ==========================

            *2位: {coins[-2][1]}*
            
            順位: {coins[-2][0]}位
            市場規模: {coins[-2][2]}
            対ドル価格: {coins[-2][3]}
            前日比: {coins[-2][4]}%
        ==========================

            *3位: {coins[-3][1]}*
            
            順位: {coins[-3][0]}位
            市場規模: {coins[-3][2]}
            対ドル価格: {coins[-3][3]}
            前日比: {coins[-3][4]}%
        ===========================

        :fire:*今日のコインワースト3*:fire:
        
        ==========================
            *1位: {coins[0][1]}*
            
            順位: {coins[0][0]}位
            市場規模: {coins[0][2]}
            対ドル価格: {coins[0][3]}
            前日比: {coins[0][4]}%
        ==========================

            *2位: {coins[1][1]}*
            
            順位: {coins[1][0]}位
            市場規模: {coins[1][2]}
            対ドル価格: {coins[1][3]}
            前日比: {coins[1][4]}%
        ==========================

            *3位: {coins[2][1]}*
            
            順位: {coins[2][0]}位
            市場規模: {coins[2][2]}
            対ドル価格: {coins[2][3]}
            前日比: {coins[2][4]}%
        ===========================
        
        参照:　https://coinmarketcap.com/
    """

    return {
        'channel': channel,
        'text': message
    }