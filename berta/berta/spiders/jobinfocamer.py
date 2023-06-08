import scrapy

from berta.items import JobItem


class JobinfocamerSpider(scrapy.Spider):
    name = "jobinfocamer"
    allowed_domains = ["www.jobinfocamer.com"]
    start_urls = ["https://www.jobinfocamer.com/jobs/Informatique/"]
    custom_settings = {
        'FEEDS': { 'data/jobinfo2.json': { 'format': 'json', 'overwrite':True}}
        }

    def parse(self, response):
        
        job_item = JobItem()
        jobs = response.css("table.table-offre-categories tr")
        
        for job in jobs:
            relative_url = job.css('a').attrib['href']
            job_url = 'https://www.jobinfocamer.com' + relative_url
            
            yield scrapy.Request(job_url, callback=self.parse_job_page)
        
        # next_page = response.css('.pagination li:nth-child(6) a ::attr(href)').get()
        # # if next_page is not None:
        # #     if 'recheche-jobs-cameroun/' in next_page:
        # next_page_url = 'https://www.jobinfocamer.com' + next_page
        # #     else:
        # #         next_page_url = 'https://books.toscrape.com/catalogue/' + next_page
        # yield response.follow(next_page_url, callback=self.parse)
        # yield job_item

    def parse_job_page(self, response):
        job = response.css(".home-detail-job")[0]
        table_rows = response.css("table tr")
        title = job.css(".headline h2::text").get()
        if 'dev' in title.lower():
            yield {
                'title' :job.css(".headline h2::text").get(),
                # 'jobDetails': ,
                # 'description': job.css(".job-description p:nth-child(2) ::text").get(),
                'employer': job.css(".detail-job tr:nth-child(1) td+ td ::text").get() ,
                'type':job.css(".search-block , .detail-job tr:nth-child(3) td:nth-child(1) ::text").get(),
                'location': job.css(".detail-job tr:nth-child(2) td:nth-child(1) ::text").get(),
                'publishedDate': job.css(".detail-job tr:nth-child(1) td:nth-child(1) ::text").get(),
                'expirationDate': job.css(".detail-job tr:nth-child(4) td:nth-child(1) ::text").get(),
                'applyLink': job.css(".job-description a").attrib['href']
            }