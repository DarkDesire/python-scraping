import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

articleUrl = "/wiki/Kevin_Bacon"
html = urlopen("http://en.wikipedia.org"+articleUrl)
bsObj = BeautifulSoup(html, 'html.parser')
bodyContent = bsObj.find('div',{'id':"bodyContent"})
for link in bodyContent.findAll("a", href=re.compile("^(/wiki/)((?!:).)*$")):
    if 'href' in link.attrs:
        print(link.attrs['href'])