import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import requests
from bs4 import BeautifulSoup

class Content:
    def __init__(self, url, title, body):
        self.title = title
        self.body = body
        self.url = url

    def pprint(self):
        print(f"{self.title=}")
        print(f"{self.body=}")
        print(f"{self.url=}")

class Website:
    def __init__(self, name, url, titleTag, bodyTag):
        self.name = name
        self.url = url
        self.titleTag = titleTag
        self.bodyTag = bodyTag

#####

import requests
from bs4 import BeautifulSoup

class Crawler:
    def getPage(self, url):
        try: 
            req = requests.get(url)
        except requests.exceptions.RequestException:
            return
        return BeautifulSoup(req.text,'html.parser')

    def safeGetInfo(self, pageObj, selector):
        selectedElems = pageObj.select(selector)
        print(selectedElems)
        if selectedElems is not None and len(selectedElems)>0:
            return "\n".join([elem.get_text() for elem in selectedElems])
        return ''
    
    def parse(self, site, url):
        bs = self.getPage(url)
        if bs is not None:
            title = self.safeGetInfo(bs, site.titleTag)
            body = self.safeGetInfo(bs, site.bodyTag)
            if title != '' and body != '':
                content = Content(url,title,body)
                content.pprint()

##### predefine
crawler = Crawler()

siteData = [
    ['Moscow 24', 'https://m24.ru/','h1','div.b-material-body div p'],
    ['Russa Today', 'https://ru.rt.com/','h1','div.article__text.article__text_article-page.js-mediator-article > p'], 
    ['1 TV RU', 'https://1tv.ru/','h1','div.editor.text-block.active > p'],
    ['RBC','https://rbc.ru/','h1','div.article__text.article__text_free > p'],
]

##### start

websites = []
for row in siteData:
    websites.append(Website(row[0],row[1],row[2],row[3]))

#crawler.parse(websites[0], 'https://www.m24.ru/news/vlast/01032022/436096')

## 'DDOS-GUARDddos_3'
##crawler.parse(websites[1], 'https://russian.rt.com/world/article/969653-ukraina-es-chlenstvo-politika')

#crawler.parse(websites[2], 'https://www.1tv.ru/news/2022-03-01/422245-s_lavrov_tsel_spetsoperatsii_rf_spasenie_lyudey_demilitarizatsiya_i_denatsifikatsiya_ukrainy')

crawler.parse(websites[3], 'https://www.rbc.ru/business/02/03/2022/621e958f9a794736ac477c51?from=from_main_1')