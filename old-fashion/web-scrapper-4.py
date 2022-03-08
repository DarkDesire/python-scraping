import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import requests
from bs4 import BeautifulSoup
from pprint import pprint

class Content:
    def __init__(self, topic, url, title, body):
        self.topic = topic
        self.title = title
        self.body = body
        self.url = url

    def pprint(self):
        print(f"{self.topic=}")
        print(f"{self.title=}")
        print(f"{self.url=}")

class Website:
    def __init__(self, name, url, searchURL, resultListing, resultURL, absoluteURL, titleTag, bodyTag):
        self.name = name
        self.url = url
        self.searchURL = searchURL
        self.resultListing = resultListing
        self.resultURL = resultURL
        self.absoluteURL = absoluteURL
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
        if selectedElems is not None and len(selectedElems)>0:
            return "\n".join([elem.get_text() for elem in selectedElems])
        return ''
    
    def search(self, topic, site):
        pageURL = site.searchURL + topic 
        bs = self.getPage(pageURL)
        searchResults = bs.select(site.resultListing)
        for result in searchResults:
            fetchedURL = result.select(site.resultURL)
            if not fetchedURL:
                return 

            url = fetchedURL[0].attrs['href'] 
            # check is url abs or relative
            if (site.absoluteURL):
                bs = self.getPage(url)
            else:
                bs = self.getPage(site.url + url)
            
            if bs is None:
                print(f"Something wrong with page url: {url}")
                return
            
            title = self.safeGetInfo(bs, site.titleTag)
            body = self.safeGetInfo(bs, site.bodyTag)

            if title != '' and body != '':
                content = Content(topic, url,title,body)
                content.pprint()

##### predefine
crawler = Crawler()

siteData = [
    # ['Moscow 24', 'https://m24.ru/','https://www.m24.ru/sphinx/?criteria=','div#SearchBody', 'p.b-materials-list__title > a', True, 'h1','div.b-material-body div p'],
    # ['Russa Today', 'https://ru.rt.com/','h1','div.article__text.article__text_article-page.js-mediator-article > p'], 
    # [ '1 TV RU', 'https://1tv.ru/','https://www.1tv.ru/search?from=1995-01-01&to=2022-03-04&q=text%3A', 'article.results', '', True,'h1','div.editor.text-block.active > p'],
    # ['РИА НОВОСТИ', 'https://ria.ru/','https://ria.ru/search/?query=','div.list-item','a.list-item__image',True,'h1.article__title','div.article__block'],
    ['Brookigns', 'https://www.brookings.edu', 'https://www.brookings.edu/search/?s=', 'div.list-content article', 'h4.title a', True, 'h1', 'div.post-body'],
]

##### start

websites = []
for row in siteData:
    websites.append(Website(row[0],row[1],row[2],row[3], row[4], row[5], row[6], row[7]))

for site in websites:
    crawler.search('Russia',site)
