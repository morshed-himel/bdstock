import scrapy


class SingleSpider(scrapy.Spider):
    name = 'SingleSpider'
    start_urls = ['https://www.dse.com.bd/displayCompany.php?name=ALARABANK']

    custom_settings = {
        'LOG_LEVEL': 'ERROR',  # CRITICAL, ERROR, WARNING, INFO, DEBUG
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_useragents.downloadermiddlewares.useragents.UserAgentsMiddleware': 500,
        },
    }

    def parse(self, r):
        item = {}

        # Last Update time
        item['info_date'] = r.css(
            '.text-right+ .topBodyHead i::text').extract_first()

        item['info_time'] = r.css(
            '.table-responsive:nth-child(6) .alt:nth-child(2) td:nth-child(2)::text').extract_first()

        # Name of the Company
        item['company_name'] = r.css(
            '.topBodyHead:nth-child(1) i::text').extract_first()

        # Trading Code
        code = r.css(
            '.shares-table th:nth-child(1)::text').extract_first()

        item['code'] = code.replace("Trading Code:", "").strip()

        # Adjusted Opening Price
        item['op'] = r.css(
            '.alt~ .alt td:nth-child(2)::text').extract_first()

        # Closing Price
        item['cp'] = r.css(
            'tr:nth-child(1) td~ td::text').extract_first()

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
            'tr:nth-child(5) td~ td::text').extract_first()

        # No. of shares traded
        # no_shares_traded = r.css(
        #     '::text').extract_first()
        item['no_shares_traded'] = "-"

        # No. of  Trades
        item['no_trades'] = r.css(
            '.alt~ .alt td:nth-child(4)::text').extract_first()

        # Market Capitalization (mn)
        item['market_cap'] = r.css(
            'tr:nth-child(7) td~ td::text').extract_first()

        yield item


def clean_number(s):

    s = s.replace(',', '').strip()

    if s == "-" or s == "":
        return 0
    else:
        f = float(s)
        return f


def get_difference(high, low):
    dif = clean_number(high) - clean_number(low)

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
