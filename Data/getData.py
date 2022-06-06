from cgi import print_arguments
from re import L
import requests
from bs4 import BeautifulSoup
import re


def SmashBrathers():
    try:
        session = requests.Session()
        response = session.get("https://smashmate.net/fighter/")
        response.raise_for_status()     # ステータスコード200番台以外は例外とする
    except (requests.exceptions.RequestException) as e:
        print(e)
    response.close()

    soup = BeautifulSoup(response.content, "html.parser")
    li = soup.select(".smashlist>a")
    with open("Data/Data_SmaBra/SmashChara.txt",mode='w') as f:
        for i in li:
            res = str(i.contents[0]).replace("\n","").replace("\t","").replace("\r","")
            f.write(res+"\n")


def ApexChara():
    try:
        session = requests.Session()
        response = session.get("https://www.ea.com/ja-jp/games/apex-legends/about/characters")
        response.raise_for_status()     # ステータスコード200番台以外は例外とする
    except (requests.exceptions.RequestException) as e:
        print(e)
    response.close()

    soup = BeautifulSoup(response.content, "html.parser")
    q = soup.select("ea-tile > h3")

    with open("Data/Data_Apex/ApexChara.txt",mode='w') as f:
        for i in q:
            res = str(i.contents[0]).replace("<b>","").replace("</b>","")
            f.write(res+"\n")

def ApexBullet():
    """
    スクレイピングするより自分でjson作った方が早そう。
    一応下のコードで武器を取得できる。
    """
    try:
        session = requests.Session()
        #武器種
        response = session.get("https://game8.jp/apex-legends/257402")
        response.raise_for_status()     # ステータスコード200番台以外は例外とする
        #アモ種
        response2 = session.get("https://game8.jp/apex-legends/371647")
        response2.raise_for_status()
    except (requests.exceptions.RequestException) as e:
        print(e)
    response.close()

    soup = BeautifulSoup(response.content, "html.parser")
    soup2 = BeautifulSoup(response2.content, "html.parser")

    BulletType0 = []
    BulletType0.append(soup.select("body > div.l-content.js-end-trigger > div.l-3col > div.l-3colMain > div.l-3colMain__center.l-3colMain__center--shadow > div.archive-style-wrapper > table:nth-child(29) > tr > td > a"))
    BulletType0.append(soup.select("body > div.l-content.js-end-trigger > div.l-3col > div.l-3colMain > div.l-3colMain__center.l-3colMain__center--shadow > div.archive-style-wrapper > table:nth-child(33) > tr > td:nth-child(1) > a"))
    BulletType0.append(soup.select("body > div.l-content.js-end-trigger > div.l-3col > div.l-3colMain > div.l-3colMain__center.l-3colMain__center--shadow > div.archive-style-wrapper > table:nth-child(36) > tr> td:nth-child(1) > a"))
    BulletType0.append(soup.select("body > div.l-content.js-end-trigger > div.l-3col > div.l-3colMain > div.l-3colMain__center.l-3colMain__center--shadow > div.archive-style-wrapper > table:nth-child(40) > tr> td:nth-child(1) > a"))
    BulletType0.append(soup.select("body > div.l-content.js-end-trigger > div.l-3col > div.l-3colMain > div.l-3colMain__center.l-3colMain__center--shadow > div.archive-style-wrapper > table:nth-child(43) > tr> td:nth-child(1) > a"))
    BulletType0.append(soup.select("body > div.l-content.js-end-trigger > div.l-3col > div.l-3colMain > div.l-3colMain__center.l-3colMain__center--shadow > div.archive-style-wrapper > table:nth-child(47) > tr> td:nth-child(1) > a"))
    BulletType0.append(soup.select("body > div.l-content.js-end-trigger > div.l-3col > div.l-3colMain > div.l-3colMain__center.l-3colMain__center--shadow > div.archive-style-wrapper > table:nth-child(50) > tr> td:nth-child(1) > a"))
    BulletType0.append(soup2.select("body > div.l-content.js-end-trigger > div.l-3col > div.l-3colMain > div.l-3colMain__center.l-3colMain__center--shadow > div.archive-style-wrapper > table:nth-child(23) > tr > td:nth-child(1) > a"))


    BulletType = ["AR","SMG","LMG","SR","SG","PT","MM","KP"]
    with open("Data/Data_Apex/ApexBullet.json",mode='w') as f:
        f.write("{")
        for i,type in enumerate(BulletType):
            if(i==0):
                f.write('"'+type+'":')
            else:
                f.write(',"'+type+'":')
            for j,value in enumerate(BulletType0[i]):
                if(j==0):
                    f.write('["'+str(value.contents[1])+'"')
                    continue
                f.write(',"'+str(value.contents[1])+'"')
            f.write(']\n')
        f.write("}")
        

SmashBrathers()