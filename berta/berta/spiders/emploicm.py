import datetime
import re
import scrapy
from berta.items import JobItem
import requests
from functools import reduce

class TrustpilotspiderSpider(scrapy.Spider):
    name = "emploicm"
    allowed_domains = ["www.emploi.cm"]
    start_urls = ["https://www.emploi.cm/recherche-jobs-cameroun"]
    custom_settings = {
        'FEEDS': { 'emploicm.json': { 'format': 'json',}}
        }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)
            
    # def parse(self, response, **kwargs):
    #     job_item = JobItem()
    #     job = response.css(".job-search-result")
    #     # for job in jobs:
    #     title_link = job.css('h5')
    #     job_item['title'] = title_link.css('a::text').extract_first()
    #     job_item['description'] = job.css('.search-description::text').extract_first()
        
    #     job_item['date'] = job.css('p.job-recruiter::text').extract_first()
    #     job_item['location'] = job.css('.search-description+p::text').extract_first()
        
    #     yield job_item
    
    def parse(self, response, **kwargs):
        job_item = JobItem()
        
        jobs = response.css(".job-search-result")
        for job in jobs:
            yield{ 
                # title_link = job.css('h5')
                'title' : job.css('h5 a ::text').get(),
                'description' : job.css('.search-description::text').get(),
                
                'date' : job.css('p.job-recruiter::text').get(),
                'location' : job.css('.search-description+p::text').get()
            }
            
        
        next_page = response.css('#jobsearch-search-results-box .last a ::attr(href)').get()
        # if next_page is not None:
        #     if 'recheche-jobs-cameroun/' in next_page:
        next_page_url = 'https://www.emploi.cm' + next_page
        #     else:
        #         next_page_url = 'https://books.toscrape.com/catalogue/' + next_page
        yield response.follow(next_page_url, callback=self.parse)
        
    def date_clean(d):
        mds = re.sub('[' ', |]', '', d)
        md = mds.split('.')
        yr = int(md[2])
        mth = int(md[1])
        day = int(md[0])
        print(md)


        _date = datetime.datetime(yr, mth, day)
        date = _date.strftime("%b-%d-%Y")

        print(date)
        return date

    # date_clean(d)