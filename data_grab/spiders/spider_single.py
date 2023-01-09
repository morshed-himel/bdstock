import scrapy
import time


class SingleSpider(scrapy.Spider):
    timestr = time.strftime("%Y-%m-%d %H-%M-%S")

    name = 'SingleSpider'
    start_urls = []
    count = 0

    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'output/' + timestr + '.csv',
        'FEED_EXPORTERS': {
            'csv': 'data_grab.exporters.MyCsvItemExporter',
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
            'dif_op_cp',
            'ltp',
            'high',
            'low',
            'dif_high_low',
            'days_vol',
            'no_shares_traded',
            'no_trades',
            'market_cap',
            'time'
        ],
    }

    def parse(self, r):
        self.count += 1

        print(str(self.count) + "/" + str(len(self.start_urls)))
        item = {}

        # Last Update time
        info_date = r.css(
            '.text-right+ .topBodyHead i::text').extract_first()

        info_time = r.css(
            '.table-responsive:nth-child(6) .alt:nth-child(2) td:nth-child(2)::text').extract_first()

        item['time'] = info_date + " " + info_time

        # Name of the Company
        item['company_name'] = r.css(
            '.topBodyHead:nth-child(1) i::text').extract_first()

        # Trading Code
        code = r.css(
            '.shares-table th:nth-child(1)::text').extract_first()

        item['code'] = code.replace("Trading Code:", "").strip()

        # Adjusted Opening Price
        item['op'] = clean_number(r.css(
            '.alt~ .alt td:nth-child(2)::text').extract_first())

        # Closing Price
        item['cp'] = clean_number(r.css(
            '.table-responsive:nth-child(6) tr:nth-child(1) td~ td::text').extract_first())

        # "Difference (Open-Closing)"
        item['dif_op_cp'] = get_difference(item['cp'], item['op'])

        # Last Traded Price
        item['ltp'] = r.css(
            '.table-responsive:nth-child(6) tr:nth-child(1) td:nth-child(2)::text').extract_first()

        # Highest Price

        high_low = get_high_low(r.css(
            '.alt td:nth-child(4)::text').extract_first())

        item['low'] = high_low[0]
        item['high'] = high_low[1]

        # "Difference (High-Low)"
        item['dif_high_low'] = get_difference(item['high'], item['low'])

        # Days Volume (mn)
        item['days_vol'] = r.css(
            'tr:nth-child(3) td~ td::text').extract_first()

        # No. of shares traded
        item['no_shares_traded'] = r.css(
            'tr:nth-child(5) td~ td::text').extract_first()

        # No. of  Trades
        item['no_trades'] = r.css(
            '.alt~ .alt td:nth-child(4)::text').extract_first()

        # Market Capitalization (mn)
        item['market_cap'] = r.css(
            'tr:nth-child(7) td~ td::text').extract_first()

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
