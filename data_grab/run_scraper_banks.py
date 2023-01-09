import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from data_grab.spiders.spider_single import SingleSpider


class Scraper:
    def __init__(self):
        settings_file_path = 'data_grab.settings'
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)

    def run_spiders(self, is_proxy_on):
        spider = SingleSpider
        self.process = CrawlerProcess(get_project_settings())

        self.process.settings.set("FEED_FORMAT", 'csv')
        self.process.settings.set("FEED_URI", 'db/output/banks.csv')

        if is_proxy_on:
            spider.custom_settings['DOWNLOADER_MIDDLEWARES'].update({
                'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
                'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
            })

        self.spiders = spider
        self.process.crawl(self.spiders)
        self.process.start()
