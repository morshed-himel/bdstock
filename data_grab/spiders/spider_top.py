import scrapy
import json


class MainSpider(scrapy.Spider):
    name = 'SpiderTop'
    start_urls = ['https://www.dse.com.bd/latest_share_price_scroll_l.php']
  
    custom_settings = {
        'LOG_LEVEL': 'ERROR',  # CRITICAL, ERROR, WARNING, INFO, DEBUG
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_useragents.downloadermiddlewares.useragents.UserAgentsMiddleware': 500,
        },
    }

    def parse(self, r):
        responce = {}
        table = r.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "fixedHeader", " " ))]//tr')
        
        responce["time"] = r.css('.topBodyHead::text').extract_first()
        responce['data'] = []
        
        for row in table:
            code = row.xpath('td[2]//text()').extract()
            
            if len(code) < 1:
                continue
            
            code = code[1].replace("\r\n","")
            code = code.replace("\t","")
            
            item = {
                'code' : code,
                'ltp': row.xpath('td[3]//text()').extract_first(),
                'high' : row.xpath('td[4]//text()').extract_first(),
                'low' : row.xpath('td[5]//text()').extract_first(),
            }

            responce['data'].append(item)
        
        json_data = json.dumps(responce)
        print(json_data)
    