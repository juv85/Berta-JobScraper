import scrapy


class CameroonDeskSpider(scrapy.Spider):
    name = "cameroon-desk"
    allowed_domains = ["'https://www.cameroondesks.com"]
    start_urls = ["https://www.cameroondesks.com/search/label/jobs"]

    def parse(self, response):
        pass
