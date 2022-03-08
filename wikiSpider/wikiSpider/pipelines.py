from datetime import datetime
from wikiSpider.items import Article
from string import whitespace

# в пайплайн передаются все объекты
class WikispiderPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, Article):
            item['lastUpdated'] = item['lastUpdated'].replace('This page was last edited on', '')
            item['lastUpdated'] = item['lastUpdated'].strip()
            item['lastUpdated'] = datetime.strptime(item['lastUpdated'], '%d %B %Y, at %H:%M.')
            print(f"{item=}")
            item['text'] = [line for line in item['text'] if line not in whitespace]
            item['text'] = ''.join(item['text'])
            print(f"{item=}")
            return item