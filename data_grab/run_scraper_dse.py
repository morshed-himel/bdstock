import os

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from data_grab.spiders.spider_single import SingleSpider
from data_grab.spiders.spider_dse_listing import ListingSpider

from twisted.internet import reactor
from twisted.internet.task import deferLater


class Scraper:
    index = -1

    def __init__(self):
        settings_file_path = 'data_grab.settings'
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)

    def run_to_get_all(self, is_proxy_on, json_array):
        print(json_array[0]["category_name"])

    def run_spider_listing(self, is_proxy_on):
        spider = ListingSpider
        self.process = CrawlerProcess(get_project_settings())
        url = 'https://www.dse.com.bd/by_industrylisting.php'
        spider.start_urls.append(url)

        if is_proxy_on:
            spider.custom_settings['DOWNLOADER_MIDDLEWARES'].update({
                'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
                'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
            })

        self.spiders = spider
        self.process.crawl(self.spiders)
        self.process.start()

    def run_spiders(self, is_proxy_on, category, bank_list):
        spider = SingleSpider
        self.process = CrawlerProcess(get_project_settings())
        spider.category = category

        for b in bank_list:
            url = 'https://www.dse.com.bd/displayCompany.php?name='+b
            spider.start_urls.append(url)

        if is_proxy_on:
            spider.custom_settings['DOWNLOADER_MIDDLEWARES'].update({
                'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
                'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
            })

        self.spiders = spider
        self.process.crawl(self.spiders)
        self.process.start()
