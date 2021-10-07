import scrapy
import json
import re

from datetime import datetime
from ..items import CarItem
from urllib.parse import urlparse, parse_qs, urlunparse, urlencode, urljoin
from helper.utils import clean_result, strip_tags

from scrapy.shell import inspect_response

# https://www.autotrader.ca/cars/bc/
# ?rcp=100&rcs=0&srt=9&prx=-2&prv=British%20Columbia&loc=V5K%200A1&hprc=True&wcp=True&sts=New-Used&inMarket=advancedSearch

# https://www.autotrader.ca/cars/bc/
# ?rcp=100&rcs=0&srt=9&prx=-2&prv=British%20Columbia&loc=V5K%200A1&hprc=True&wcp=True&sts=Used&adtype=Private&inMarket=advancedSearch

# https://www.autotrader.ca/a/19_11609815


def get_data_from_list(d_list, clue):
    val = "-"

    for data in d_list:
        if data.get("key") == clue:
            val = data.get("value")
            break
    return val


# todo Validate Link
def determine(image_link):
    if len(image_link) < 15:
        return False

    return True


class MainSpider(scrapy.Spider):
    name = 'MainSpider'
    count = 0
    start_urls = [
        'https://www.autotrader.ca/cars/bc/?rcp=100&rcs=0&srt=9&prx=-2&prv=British%20Columbia&loc=V5K%200A1&hprc=True&wcp=True&sts=Used&adtype=Private&inMarket=advancedSearch'
    ]
    custom_settings = {
        'FEED_URI': 'db/output/autotrader_personal_listing.csv',
        'LOG_LEVEL': 'INFO',  # CRITICAL, ERROR, WARNING, INFO, DEBUG
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware':
            None,
            'scrapy_useragents.downloadermiddlewares.useragents.UserAgentsMiddleware':
            500,
        },
    }

    def parse(self, response):
        parsed = urlparse(response.url)

        query_dict = parse_qs(parsed.query)
        query_dict.get('rcs')[0] = int(query_dict['rcs'][0]) + 100

        new_query = urlencode(query_dict, doseq=True)
        replaced = parsed._replace(query=new_query)
        next_page_url = urlunparse(replaced)

        totalCarCount = response.css('#sbCount::text').extract_first()

        if totalCarCount:
            totalCarCount = (int(totalCarCount.replace(",", "")) + 4)
        else:
            totalCarCount = 0

        try:
            dump = re.compile(r'"vehicles":(\[{.*?}])',
                              re.MULTILINE | re.DOTALL)

            vehicles = response.xpath(
                '//script[contains(., "var gtmManager;")]/text()').re(dump)[0]
            vehicles = json.loads(vehicles)

            total = len(vehicles)

            if total <= 0:
                print("Done on last page")
                return

            for vehicle in vehicles:
                item = CarItem()
                link = "https://www.autotrader.ca/a/" + \
                    vehicle.get('adID') + "_/"
                u = link.replace("-", "_")

                item['stock_no'] = vehicle.get('adID')
                item['make'] = vehicle.get('make')
                item['model'] = vehicle.get('model')
                item['year'] = vehicle.get('year')
                item['condition'] = vehicle.get('condition')
                item['dealer_id'] = "autoTRADER"

                item['title'] = item['year'] + " " + \
                    item['make'] + " " + item['model']

                request = scrapy.Request(u, callback=self.parse_details)
                request.meta['item'] = item
                yield request

            if query_dict.get('rcs')[0] < totalCarCount:
                yield scrapy.Request(url=next_page_url, callback=self.parse)

        except:
            print("denied at >> ", response.url)

            if query_dict.get('rcs')[0] < totalCarCount:
                yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse_details(self, response):
        item = response.meta['item']

        self.count += 1
        item['url'] = response.url
        item['scrap_date'] = datetime.today().strftime('%Y-%m-%d %H:%M')

        dump = re.compile(r"window\['ngVdpModel'] = ({.*?};)",
                          re.MULTILINE | re.DOTALL)

        try:
            data = response.xpath(
                '//script[contains(., "window[\'ngVdpModel\']")]/text()').re(
                    dump)[0]

            vehicle_data = json.loads(data.replace(";", ""))

            details_table = vehicle_data.get('specifications')['specs']

            item['stock_no'] = vehicle_data.get('adBasicInfo')['adId']
            
            pf_link = urlparse(vehicle_data.get('privateFinanceLink'))
            q_dict = parse_qs(pf_link.query)
            
            item['vin'] = q_dict.get('vin')


            item['trim'] = vehicle_data.get('adBasicInfo')['trim']
            item['body'] = vehicle_data.get('adBasicInfo')['splashBodyType']
            item['odometer'] = vehicle_data.get('hero')['mileage']
            item['retail'] = vehicle_data.get('adBasicInfo')['price']
            item['sale'] = "-"
            item['sold'] = "-"
            item['description'] = vehicle_data.get(
                'description')['description']
            item['doors'] = get_data_from_list(details_table, 'Doors')
            item['passengers'] = "-"
            item['fueltype'] = get_data_from_list(details_table, 'Fuel Type')
            item['engine'] = "-"
            item['drivetrain'] = get_data_from_list(details_table,
                                                    'Drivetrain')
            item['transmission'] = get_data_from_list(details_table,
                                                    'Transmission') 
            item['color_int'] = "-"
            item['color_ext'] = get_data_from_list(details_table,
                                                    'Exterior Colour')
            item['economy_city'] = "-"
            item['economy_hwy'] = "-"

            images = vehicle_data.get('gallery')['items']

            if len(images) > 0:
                firstImage = True
                img_str = ""

                for img in images:
                    if firstImage:
                        firstImage = False
                    else:
                        img_str += "|"

                    img_str += img.get("galleryUrl").replace("-1024x786", "")

                item['images'] = img_str
            else:
                item['images'] = "-"

            item['latitude'] = vehicle_data.get('deepLinkSavedSearch')['savedSearchCriteria']['location']['latitude']
            item['longitude'] = vehicle_data.get('deepLinkSavedSearch')['savedSearchCriteria']['location']['longitude']
            item['city'] = vehicle_data.get('deepLinkSavedSearch')['savedSearchCriteria']['city']
            item['province'] = vehicle_data.get('deepLinkSavedSearch')['savedSearchCriteria']['provinceAbbreviation']

        except:
            # LOG ERROR
            print("Prob at >>> ", response.url)
        finally:
            print(self.count, " >>> ", item['title'])
            yield item
