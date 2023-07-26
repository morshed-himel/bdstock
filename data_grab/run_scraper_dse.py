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
        self.process = CrawlerProcess(get_project_settings())

    def sleep(self, *args, seconds):
        """Non blocking sleep callback"""
        return deferLater(reactor, seconds, lambda: None)

    def crash(self, failure):
        print('oops, spider crashed')
        print(failure.getTraceback())

    def _crawl(self, result, spider, json_array):
        self.index += 1
        print(">> Starting index >>", self.index)

        spider.category = json_array[self.index]["category_name"]
        spider.start_urls = []

        c_list = json_array[self.index]["catalog"]

        for c in c_list:
            url = 'https://www.dse.com.bd/displayCompany.php?name=' + c
            spider.start_urls.append(url)

        deferred = self.process.crawl(spider)
        deferred.addCallback(lambda results: print(
            'waiting 2 seconds before restart...'))
        deferred.addErrback(self.crash)  # <-- add errback here
        deferred.addCallback(self.sleep, seconds=2)
        deferred.addCallback(self._crawl, spider, json_array)
        return deferred

    def run_to_get_all(self, is_proxy_on, json_array):
        self.index += 1
        spider = SingleSpider
        spider.category = json_array[self.index]["category_name"]
        spider.start_urls = []

        c_list = json_array[self.index]["catalog"]

        for c in c_list:
            url = 'https://www.dse.com.bd/displayCompany.php?name=' + c
            spider.start_urls.append(url)

        if is_proxy_on:
            spider.custom_settings['DOWNLOADER_MIDDLEWARES'].update({
                'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
                'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
            })

        self._crawl(None, spider, json_array)
        self.process.start()

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

    def run_spiders(self, is_proxy_on, category, c_list):
        spider = SingleSpider
        self.process = CrawlerProcess(get_project_settings())
        spider.category = category
        spider.start_urls = []

        for c in c_list:
            url = 'https://www.dse.com.bd/displayCompany.php?name=' + c
            spider.start_urls.append(url)

        if is_proxy_on:
            spider.custom_settings['DOWNLOADER_MIDDLEWARES'].update({
                'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
                'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
            })

        self.spiders = spider
        self.process.crawl(self.spiders)
        self.process.start()
