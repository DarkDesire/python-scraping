# 1
class Website:
    def __init__(self, name, url, titleTag, bodyTag, pageType):
        self.name = name
        self.url = url
        self.titleTag = titleTag
        self.bodyTag = bodyTag
        self.pageType = pageType

#2 
class Website:
    def __init__(self, name, url, titleTag):
        self.name = name
        self.url = url
        self.titleTag = titleTag

class Product(Website):
    def __init__(self, name, url, titleTag, productNumberTag, priceTag):
        super().__init__(name, url, titleTag)
        self.productNumberTag = productNumberTag
        self.priceTag = priceTag

class Article(Website):
    def __init__(self, name, url, titleTag, bodyTag, dateTag):
        super().__init__(name, url, titleTag)
        self.bodyTag = bodyTag
        self.dateTag = dateTag