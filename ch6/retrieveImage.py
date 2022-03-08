import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from urllib.request import urlretrieve
from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen('http://www.pythonscraping.com')
bsObj = BeautifulSoup(html, 'html.parser')
imageLocation = bsObj.find('img', {'class': 'pagelayer-img pagelayer-wp-title-img'})['src']
urlretrieve (imageLocation, 'logo.jpg')