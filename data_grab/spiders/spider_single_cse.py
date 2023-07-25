import scrapy
import time


class SingleSpiderCSE(scrapy.Spider):
    time_str = time.strftime("%d-%m-%Y %H-%M-%S")

    name = 'SingleSpiderCSE'
    start_urls = []
    count = 0

    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'output/cse_' + time_str + '.csv',
        'FEED_EXPORTERS': {
            'csv': 'data_grab.exporters.cseItemExporter',
        },
        'ITEM_PIPELINES': {
            'data_grab.pipelines.DataGrabPipeline': 300,
        },
        'LOG_LEVEL': 'ERROR',  # CRITICAL, ERROR, WARNING, INFO, DEBUG
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_useragents.downloadermiddlewares.useragents.UserAgentsMiddleware': 500,
        },
        'FEED_EXPORT_FIELDS': [
            'company_name',
            'code',
            'op',
            'cp',
            'ltp',
            'high',
            'low',
            'days_vol',
            'no_trades',
            'market_cap',
            'auth_cap',
            'paid_cap',
            'face_val',
            'paid_shr',
            'time'
        ],
    }

    def parse(self, r):
        self.count += 1
        print(str(self.count) + "/" + str(len(self.start_urls)))
        item = {}

        # Last Update time
        info_date = r.css(
            '.rightfloat:nth-child(2)::text').extract_first()

        info_time = r.css(
            '.rightfloat~ .rightfloat+ .rightfloat::text').extract_first()

        item['time'] = clean_text(info_date + " " + info_time, "\xa0")

        # Name of the Company
        item['company_name'] = r.css(
            '.com_title::text').extract_first()

        # Trading Code
        item['code'] = r.css(
            '.col_5 b+ b::text').extract_first()

        # Adjusted Opening Price
        item['op'] = r.css(
            'td td:nth-child(1) tr:nth-child(4) td+ td::text').extract_first()

        # Closing Price
        item['cp'] = r.css(
            'td+ td tr:nth-child(3) td+ td::text').extract_first()

        # Last Traded Price
        item['ltp'] = r.css(
            'td td tr:nth-child(1) td+ td::text').extract_first()

        item['ltp'] = clean_text(item['ltp'], "\n")
        item['ltp'] = clean_text(item['ltp'], "\t")

        # Highest Price
        high_low = get_high_low(r.css(
            'tr:nth-child(5) td+ td::text').extract_first())

        item['low'] = high_low[0]
        item['high'] = high_low[1]

        # Days Volume (mn)
        item['days_vol'] = r.css(
            "td+ td tr+ tr td+ td::text").extract_first()

        # No. of  Trades
        item['no_trades'] = r.css(
            'table:nth-child(1) table td+ td tr:nth-child(1) td+ td::text').extract_first()

        # Market Capitalization (mn)
        item['market_cap'] = r.css(
            'td+ td tr:nth-child(5) td+ td::text').extract_first()

        # Authorized Capital in BDT* (mn)
        item['auth_cap'] = r.css(
            'table+ table table table tr:nth-child(1) td+ td::text').extract_first()

        # Paid-up Capital in BDT* (mn)
        item['paid_cap'] = r.css(
            'table~ table+ table table td:nth-child(1) tr:nth-child(2) td+ td::text').extract_first()

        # Face Value
        item['face_val'] = r.css(
            'table~ table+ table table tr:nth-child(3) td+ td::text').extract_first()

        # Paid up Share
        item['paid_shr'] = r.css(
            'table~ table+ table tr:nth-child(4) td+ td::text').extract_first()

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


def clean_text(s, y):
    if isinstance(s, str):
        s = s.replace(y, '').strip()

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
