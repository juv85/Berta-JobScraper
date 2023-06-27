
import scrapy
from berta.items import JobItem

import translate

from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, ConnectionRefusedError, TimeoutError

# options = Options()
# options.headless = True
# options.add_argument("--window-size=1920,1200")

# driver = webdriver.Firefox(options=options, executable_path='../geckodriver.exe')


class JobinfocamerSpider(scrapy.Spider):
    name = "jobinfocamer"
    allowed_domains = ["www.jobinfocamer.com"]
    start_urls = ["https://www.jobinfocamer.com/"]
    custom_settings = {
        'FEEDS': { 'data/jobinfo2.json': { 'format': 'json'}}
        }
    
    

    def parse(self, response):
        
        search_query = 'developer, yaounde' # enter your search query here
        yield scrapy.FormRequest.from_response(
            response,
            formdata={'job-search': search_query},
            callback=self.parse_result
        )
        
    def parse_result(self, response):
        
        jobs = response.css("table.table-offre-categories tr")
        
        # enter the search query and submit the search
        
        for job in jobs:
            relative_url = job.css('a').attrib['href']
            job_url = 'https://www.jobinfocamer.com' + relative_url
            
            yield scrapy.Request(job_url, callback=self.parse_job_page)
            # yield SeleniumRequest(url=job_url, callback=self.parse)
        
        # next_page = response.css('.pagination li:nth-child(6) a ::attr(href)').get()
        # next_page_url = 'https://www.jobinfocamer.com' + next_page
        # yield response.follow(next_page_url, callback=self.parse)
        
    def parse_job_page(self, response):
        translator = translate.Translator(to_lang='en')
        
        job = response.css(".home-detail-job")[0]
        # table_rows = response.css("table tr")
        # title = job.css(".headline h2::text").get()
        description = response.css('div.job-description ::text').getall()
        
        job_name = job.css(".headline h2::text").get()
        job_description = ''.join(description).strip()
        
        job_description = job_description.replace('\r\n', '<br>')
        job_description = job_description.replace('\n', '<br>')
        
        employer = job.css(".detail-job tr:nth-child(1) td+ td ::text").get()
        job_type = job.css(".search-block , .detail-job tr:nth-child(3) td:nth-child(1) ::text").get()
        job_location = job.css(".detail-job tr:nth-child(2) td:nth-child(1) ::text").get()
        pub_date = job.css(".detail-job tr:nth-child(1) td:nth-child(1) ::text").get()
        exp_date = job.css(".detail-job tr:nth-child(4) td:nth-child(1) ::text").get()
        apply_link = job.css(".job-description a").attrib['href']
        
        job_name_en = translator.translate(job_name)
        job_description_en = translator.translate(job_description)
        # employer_en = translator.translate(employer)
        job_type_en = translator.translate(job_type)
        
        yield {
            'title' : job_name_en,
            # 'jobDetails': ,
            'description': job_description_en,
            'employer': employer,
            'type': job_type_en,
            'location': job_location,
            'publishedDate': pub_date,
            'expirationDate': exp_date,
            'applyLink':apply_link 
        }
        
    # def start_requests(self):
    #     # Click on the search button to submit the search form
    #     yield scrapy.Request(
    #         url='https://www.jobinfocamer.com/',
    #         callback=self.parse
    #     )

        
    # def handle_httpstatus_list(self, response, exception):
    #     self.logger.info('Ignoring response %s: HTTP status code is not handled or not allowed ', response)
    #     if response.status == 404:
    #         self.logger.info('Received a 404 error for URL %s', response.url)
            
    def handle_error(self, failure):
        if failure.check(HttpError):
            response = failure.value.response
            self.logger.error('HTTP error %s on %s', response.status, response.url)
        elif failure.check(DNSLookupError):
            request = failure.request
            self.logger.error('DNS lookup failed on %s', request.url)
        elif failure.check(ConnectionRefusedError):
            request = failure.request
            self.logger.error('Connection refused on %s', request.url)
        elif failure.check(TimeoutError):
            request = failure.request
            self.logger.error('Timeout error on %s', request.url)
        else:
            request = failure.request
            self.logger.error('Error on %s', request.url, failure.value)