"""
Indeed Job Crawler
"""

import scrapy
import datetime as dt

search_term = 'data science'
city = 'pittsburgh'
state = 'pa'

class IndeedSpider(scrapy.Spider):
    name = 'Indeed Creepy Crawler'
    allowed_domains = ['indeed.com']
    start_urls = ["https://www.indeed.com/jobs?q={}&l={}%2C%20{}&jt=fulltime&start=0".format(search_term, city, state)]

    def parse(self, response):
        for jk in response.xpath("//*[contains(@class, 'row  result')]/@data-jk").extract():
            yield scrapy.Request('https://www.indeed.com/viewjob?jk={}'.format(str(jk)), callback=self.parse_job_post)

    def parse_job_post(self, response):
        yield {
            'job_title': response.xpath("//b[@class='jobtitle']/font//text()").extract_first(),
            'company': response.xpath("//*[@class='company']//text()").extract_first(),
            'location': response.xpath("//*[@class='location']//text()").extract_first(),
            'summary_1': response.xpath("//*[@id='job_summary']//text()").extract(),
            'summary_2': response.xpath("//span[contains(@class, 'summary')]//text()").extract(),
            'summary_3': response.xpath("//span[contains(@id, 'job_summary')]//text()").extract(),
            'date': response.xpath("//*[@class='date']//text()").extract_first(),
            'url': response.url,
            'timestamp': str(dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        }
