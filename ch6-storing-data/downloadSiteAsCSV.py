import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen('http://en.wikipedia.org/wiki/Comparison_of_text_editors')
bs = BeautifulSoup(html, 'html.parser')
# The main comparison table is currently the first table on the page
table = bs.findAll('table',{'class':'wikitable'})[0]
rows = table.findAll('tr')

with open('editors.csv', 'wt+', encoding='utf-8') as csvFile:
    writer = csv.writer(csvFile, delimiter=',', lineterminator='\n')
    for row in rows:
        csvRow = []
        for cell in row.findAll(['td', 'th']):
            csvRow.append(cell.get_text().strip())
        writer.writerow(csvRow)