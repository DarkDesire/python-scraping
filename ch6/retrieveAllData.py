import os
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from urllib.request import urlretrieve
from urllib.request import urlopen
from bs4 import BeautifulSoup

downloadDirectory = 'downloaded'
baseUrl = 'https://pythonscraping.com'

def getAbsoluteURL(baseUrl, source):
    if source.startswith('https://www.'):
        url = 'https://{}'.format(source[11:])
    elif source.startswith('https://'):
        url = source
    elif source.startswith('www.'):
        url = source[5:]
        url = 'https://{}'.format(source)
    else:
        url = '{}/{}'.format(baseUrl, source)
    if baseUrl not in url:
        return
    return url

def getDownloadPath(baseUrl, absoluteUrl, downloadDirectory):
    path = absoluteUrl.replace('www.', '')
    path = path.replace(baseUrl, '')
    path = path.split('?')[0]
    path = downloadDirectory+path
    directory = os.path.dirname(path)

    if not os.path.exists(directory):
        os.makedirs(directory)

    return path

html = urlopen('https://www.pythonscraping.com')
bs = BeautifulSoup(html, 'html.parser')
downloadList = bs.findAll(src=True)

for download in downloadList:
    fileUrl = getAbsoluteURL(baseUrl, download['src'])
    if fileUrl is not None:
        print(fileUrl)

    urlretrieve(fileUrl, getDownloadPath(baseUrl, fileUrl, downloadDirectory))