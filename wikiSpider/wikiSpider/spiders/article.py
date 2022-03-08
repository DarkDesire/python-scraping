import scrapy

class ArticleSpider(scrapy.Spider):
    name='article'
    allowed_domains = ['en.wikipedia.com']
    start_urls = [
        'https://en.wikipedia.org/wiki/Python_(programming_language)', 
        'https://en.wikipedia.org/wiki/Functional_programming', 
        'https://en.wikipedia.org/wiki/Monty_Python',
    ]
    
    def parse(self, response):
        url = response.url
        title = response.css('h1::text').extract_first()
        print(f"URL is: {url}")
        print(f"Title is: {title}")

