import scrapy
import os
import json
import datetime as dt
import logging

search_term = 'data science'

page_depth = 3

project_path = os.path.join(os.sep, 'C:\\', 'work', 'ds_job_market')

log_path = os.path.join(os.sep, project_path, 'logs')

log_filename = 'indeed_crawl_log_{}'.format(
    dt.datetime.now().strftime('%Y.%m.%d_%H.%M.%S'))

logging.basicConfig(filename=os.path.join(
    os.sep, log_path, log_filename), filemode='w', level=logging.DEBUG)

logger = logging.getLogger('indeed_crawl_log')

result_path = os.path.join(os.sep, project_path, 'results')

result_filename = 'indeed_crawl_results_{}.json'.format(
    dt.datetime.now().strftime('%Y.%m.%d_%H.%M.%S'))

raw_html_path = os.path.join(os.sep, project_path, 'results', 
    'raw_html', '{}'.format(dt.datetime.now().strftime('%Y.%m.%d_%H.%M.%S')))

if not os.path.exists(raw_html_path):
    os.makedirs(raw_html_path)

# location_file = os.path.join(os.sep, project_path, 'data_science_job_market', 'locations.json')

# with open(location_file) as location_json:
#     locations = json.load(location_json)

locations = [
	{
	    'city': "Pittsburgh",
	    'state': "PA"
	},
	{
	    'city': "New York", 
	    'state': "NY"
	}
]

city_urls = []

for location in locations:
    for page in range(0, (10*page_depth), 10):
        city_urls.append(("https://www.indeed.com/jobs?q={}&l={}%2C%20{}&jt=fulltime&start={}".format(
            search_term, location['city'], location['state'], str(page))).replace(' ', '%20'))

class IndeedSpider(scrapy.Spider):
    name = "indeed_creepy_crawler"
    custom_settings = {
        'FEED_URI': os.path.join(os.sep, result_path, result_filename),
        'FEED_FORMAT': 'json',
    }
    DOWNLOAD_DELAY = 0.5
    allowed_domains = ['indeed.com']
    start_urls = city_urls

    def parse(self, response):
        for jk in response.xpath("//*[contains(@class, 'row  result')]/@data-jk").extract():
            yield scrapy.Request('https://www.indeed.com/viewjob?jk={}'.format(str(jk)), callback=self.parse_job_post)

    def parse_job_post(self, response):
        filename = response.url.split("/")[-1] + '.html'
        with open(os.path.join(os.sep, raw_html_path, filename), 'wb') as f:
            f.write(response.body)
        yield {
            'job_title': response.xpath("//b[@class='jobtitle']/font//text()").extract()[0],
            'company': response.xpath("//*[@class='company']//text()").extract()[0],
            'location': response.xpath("//*[@class='location']//text()").extract()[0],
            'summary_1': response.xpath("//*[@id='job_summary']//text()").extract(),
            'summary_2': response.xpath("//span[contains(@class, 'summary')]//text()").extract(),
            'summary_3': response.xpath("//span[contains(@id, 'job_summary')]//text()").extract(),
            'date': response.xpath("//*[@class='date']//text()").extract()[0],
            'url': response.url,
            'timestamp': str(dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        }
