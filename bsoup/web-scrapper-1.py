import ssl
ssl._create_default_https_context = ssl._create_unverified_context


from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re
import datetime
import random

pages = set()
random.seed(datetime.datetime.now())

# get all internal links on page
def getInternalLinks(bs, includeUrl):
    includeUrl = '{}://{}'.format(
        urlparse(includeUrl).scheme, 
        urlparse(includeUrl).netloc
    )
    internalLinks = []
    # find all started with /
    for link in bs.find_all('a', href=re.compile('^(/|.*'+includeUrl+')')):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in internalLinks:
                if(link.attrs['href'].startswith('/')):
                    internalLinks.append(includeUrl+link.attrs['href'])
                else:
                    internalLinks.append(link.attrs['href'])
    
    return internalLinks


def getExternalLinks(bs, excludeUrl):
    externalLinks = []
    # find all links, that starts with "http" or "https"
    # and don't include current URL
    for link in bs.find_all('a', href=re.compile('^(www|http)((?!'+excludeUrl+').)*$')):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in externalLinks:
                externalLinks.append(link.attrs['href'])
    return externalLinks

def getRandomExternalLink(startingPage):
    html = urlopen(startingPage)
    bs = BeautifulSoup(html, 'html.parser')
    externalLinks = getExternalLinks(bs,
        urlparse(startingPage).netloc
    )
    if len(externalLinks) == 0:
        print('No external links, looking around the site for one')
        domain = '{}://{}'.format(
            urlparse(startingPage).scheme,
            urlparse(startingPage).netloc    
        )
        internalLinks = getInternalLinks(bs, domain)
        return getRandomExternalLink(internalLinks[random.randint(0, len(internalLinks) - 1)])
    else:
        return externalLinks[random.randint(0, len(externalLinks) -1)]

def followExternalOnly(startingSite):
    extenalLink = getRandomExternalLink(startingSite)
    print('\nRandom external link is: {}'.format(extenalLink))
    
# start
#followExternalOnly('http://oreilly.com')

allExtLinks = set()
allIntLinks = set()

def getAllExternalLinks(siteURL):
    html = urlopen(siteURL)
    bs = BeautifulSoup(html, 'html.parser')
    domain = '{}://{}'.format(
        urlparse(siteURL).scheme,
        urlparse(siteURL).netloc    
    )
    internalLinks = getInternalLinks(bs, domain)
    externalLinks = getExternalLinks(bs, domain)

    for link in externalLinks:
        if link not in allExtLinks:
            allExtLinks.add(link)
            print('External link added: {}'.format(link))
    for link in internalLinks:
        if link not in allIntLinks:
            allIntLinks.add(link)
            print('Internal link added: {}'.format(link))
            getAllExternalLinks(link)
    
allIntLinks.add('http://oreilly.com')
getAllExternalLinks('http://oreilly.com')
