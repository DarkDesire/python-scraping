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
        print(f"Parsed. {self.url}")

class Website:
    def __init__(self, name, url, targetPattern, absoluteURL, titleTag, bodyTag):
        self.name = name
        self.url = url
        self.targetPattern = targetPattern
        self.absoluteURL = absoluteURL
        self.titleTag = titleTag
        self.bodyTag = bodyTag

#####

import requests
import re
from bs4 import BeautifulSoup

class Crawler:
    def __init__(self, site):
        self.site = site
        self.visited = []

    def getPage(self, url):
        try: 
            req = requests.get(url)
        except requests.exceptions.RequestException:
            return
        return BeautifulSoup(req.text,'html.parser')

    def safeGet(self, pageObj, selector):
        selectedElems = pageObj.select(selector)
        if selectedElems is not None and len(selectedElems)>0:
            return "\n".join([elem.get_text() for elem in selectedElems])
        return ''
    
    def parse(self, url):
        bs = self.getPage(url)
        if bs is not None:
            title = self.safeGet(bs, self.site.titleTag)
            body = self.safeGet(bs, self.site.bodyTag)
            if title != '' and body != '':
                content = Content(url,title,body)
                content.pprint()

    def crawl(self):
        bs = self.getPage(self.site.url)
        targetPages = bs.find_all('a', href=re.compile(self.site.targetPattern))
        for targetPage in targetPages:
            targetPage = targetPage.attrs['href']
            if targetPage not in self.visited:
                self.visited.append(targetPage)
                if not self.site.absoluteURL:
                    targetPage = '{}{}'.format(self.site.url, targetPage)
                
                self.parse(targetPage)

##### predefine

reuters = Website('Reuters', 'https://www.reuters.com', '^(/business/)|(/world/)', False, 'h1', 'div.article-body__content__3VtU3.paywall-article')
crawler = Crawler(reuters)
crawler.crawl()