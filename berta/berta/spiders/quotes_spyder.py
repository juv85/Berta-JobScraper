from pathlib import Path

import scrapy


class AnimeQuotesSpider(scrapy.Spider):
    name = "animequotes"
    start_urls = ['https://www.goalcast.com/anime-quotes/']
    
    def parse(self, response):
         for quote in response.css(".wp-block-quote"):
            yield {
                "text": quote.css("p::text").get(),
                "author": quote.css("cite::text").get(),
            }
            
            
# wp-block-quote
class PositiveQuotesSpider(scrapy.Spider):
    name = "positivequotes"
    start_urls = ['https://blog.goalmap.com/citations-motivation/']
    
    def parse(self, response):
         for quote in response.css(".wp-block-quote"):
            yield {
                "text": quote.css("p::text").get(),
                "author": quote.css("cite::text").get(),
            }
            
