"""
Indeed Job Crawler
"""

import os
from pathlib import Path
import json
import scrapy
import random
import datetime as dt

file_path = Path(os.path.dirname(os.path.realpath(__file__)))

with open(file_path.parent.parent / 'cities.json') as f:
    cities = json.load(f)

search_term = 'data scientist'

page_depth = 10

urls = []

for location in cities:
    for page in range(0, page_depth, 1):
        urls.append("https://www.indeed.com/jobs?q={}&l={}%2C%20{}&jt=fulltime&start={}0".format(
            search_term, cities[location]['city'], cities[location]['state'], page))

class IndeedSpider(scrapy.Spider):
    name = 'Indeed Creepy Crawler'
    allowed_domains = ['indeed.com']
    start_urls = urls
    download_delay = (random.randrange(1, 200) / 1000)

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
