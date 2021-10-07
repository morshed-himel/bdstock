import scrapy
import json
import re

from datetime import datetime
from ..items import CarItem
from urllib.parse import urlparse, parse_qs, urlunparse, urlencode, urljoin
from helper.utils import clean_result, strip_tags


def get_data_from_list(d_list, clue):
    val = "-"

    for d in d_list:
        if clue in d:
            val = d.replace(clue, "").strip()
            break

    return val


# todo Validate Link
def determine(image_link):
    if len(image_link) < 15:
        return False

    return True


class MainSpider(scrapy.Spider):
    name = 'MainSpider'
    start_urls = []
   
    curr_city = ""
    count = 0

    custom_settings = {
        'FEED_URI': 'db/output/craigslist_personal_listing.csv',
        'LOG_LEVEL': 'INFO',  # CRITICAL, ERROR, WARNING, INFO, DEBUG
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware':
            None,
            'scrapy_useragents.downloadermiddlewares.useragents.UserAgentsMiddleware':
            500,
        },
    }

    def parse(self, response):
        p = {
            'entry': '.result-row',
            'entry_url': '.hdrlnk::attr(href)',
            'nav_btn': '.next',
            'btn_text': 'a::attr(title)',
            'next_text': 'next page',
            'next_url': 'a::attr(href)',
        }

        list_item = response.css(p.get('entry'))

        if len(list_item) < 1:
            print(">> NO item found")
            return

        for items in list_item:
            details_link = items.css(p.get('entry_url')).extract_first()
            url = response.urljoin(details_link)

            yield scrapy.Request(url=url, callback=self.parse_details)

            nav_btn = response.css(p.get('nav_btn'))

            for nb in nav_btn:
                btn_text = nb.css(p.get('btn_text')).extract_first()

                if btn_text == p.get('next_text'):
                    next_page_url = nb.css(p.get('next_url')).extract_first()
                    next_page_url = response.urljoin(next_page_url)

                    yield scrapy.Request(url=next_page_url,
                                         callback=self.parse)

    def parse_details(self, response):
        self.count += 1
        details_table = response.css('.attrgroup span').extract()

        for idx, a in enumerate(details_table):
            details_table[idx] = strip_tags(a)

        item = CarItem()
        item['url'] = response.url

        item['dealer_id'] = "Craigslist"

        item['stock_no'] = clean_result(
            response.css('.postinginfo:nth-child(1)').extract_first(),
            ['post id:'])

        item['vin'] = get_data_from_list(details_table, 'VIN:')
        item['condition'] = get_data_from_list(details_table, 'condition:')
        item['trim'] = "-"
        item['body'] = get_data_from_list(details_table, 'type:')
        item['odometer'] = get_data_from_list(details_table, 'odometer:')
        item['retail'] = clean_result(
            response.css('.price').extract_first(), ['$', ','])

        item['sale'] = "-"
        item['sold'] = "-"
        item['description'] = response.css('#postingbody').extract_first()
        item['doors'] = "-"
        item['passengers'] = "-"
        item['fueltype'] = get_data_from_list(details_table, 'fuel:')
        item['engine'] = get_data_from_list(details_table, 'cylinders:')
        item['drivetrain'] = get_data_from_list(details_table, 'drive:')
        item['transmission'] = get_data_from_list(details_table,
                                                  'transmission:')

        item['color_int'] = "-"
        item['color_ext'] = get_data_from_list(details_table, 'paint color:')
        item['economy_city'] = "-"
        item['economy_hwy'] = "-"

        latlon = response.xpath(
            "//meta[@property='geo.position']/@content")[0].extract()

        item['latitude'] = latlon.split(';')[0]
        item['longitude'] = latlon.split(';')[1]
        item['city'] = response.xpath(
            "//meta[@property='geo.placename']/@content")[0].extract()
        item['province'] = response.xpath(
            "//meta[@property='geo.region']/@content")[0].extract()

        item['province'] = item['province'].replace("CA-", "")

        images = response.css('#thumbs a::attr(href)').extract()

        if len(images) > 0:
            img_str = ""
            notFirstImage = False

            for i, s in enumerate(images):

                if notFirstImage:
                    img_str += "|"
                else:
                    notFirstImage = True

                img_str += images[i]

            item['images'] = img_str

        else:
            item['images'] = "-"

        part_title = str(details_table[0]).split(" ")
        try:
            item['year'] = part_title[0]

            if item['year'] == part_title[1]:
                item['make'] = part_title[2]
            else:
                item['make'] = part_title[1]

            item['model'] = details_table[0].replace(item['year'], "")
            item['model'] = str(item['model'].replace(item['make'],
                                                      "")).strip()
        except:
            item['year'] = item['make'] = item['model'] = "-"

        #########################

        item['title'] = details_table[0]
        item['scrap_date'] = datetime.today().strftime('%Y-%m-%d %H:%M')

        # item['craigslist_city'] = self.curr_city

        print(self.count, " >>> ", item['title'])
        yield item
