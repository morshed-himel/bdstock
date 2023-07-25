import scrapy
import time

from config import BASE_URL_DSE, JSON_PATH_DSE_LISTING


class ListingSpider(scrapy.Spider):
    timestr = time.strftime("%d-%m-%Y %H-%M-%S")

    name = 'ListingSpider'
    start_urls = []
    count = 0

    custom_settings = {
        'FEED_URI': JSON_PATH_DSE_LISTING,
        'FEED_FORMAT': 'json',
        'LOG_LEVEL': 'ERROR',  # CRITICAL, ERROR, WARNING, INFO, DEBUG
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_useragents.downloadermiddlewares.useragents.UserAgentsMiddleware': 500,
        }
    }

    def parse(self, r):
        category_names = r.css(
            '.txt-al-l .ab1::text').extract()
        category_links = r.css(
            '.txt-al-l a::attr(href)').extract()

        for i, (name, link) in enumerate(zip(category_names, category_links)):
            item = dict()

            item['category_name'] = name
            item['category_link'] = link

            request = scrapy.Request(BASE_URL_DSE + link,
                                     callback=self.parse_category,
                                     cb_kwargs=dict(item=item))
            yield request

    def parse_category(self, response, item):
        item['catalog'] = response.css(
            '.background-white .ab1::text').extract()

        yield item


def clean_number(s):
    if isinstance(s, str):
        s = s.replace(',', '').strip()

        if s == "-" or s == "":
            return 0
        else:
            f = float(s)
            return f
    else:
        return s


def get_difference(high, low):
    dif = round(clean_number(high) - clean_number(low), 2)

    if dif == 0:
        return "-"
    else:
        return dif


def get_high_low(s):
    if s == "-":
        return ["-", "-"]
    else:
        val = s.split("-")
        return [clean_number(val[0]), clean_number(val[1])]
