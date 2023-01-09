import scrapy

class CarItem(scrapy.Item):
    dealer_id = scrapy.Field() # Dealer Id identifier for composite feed, dealer inventory feed can be distinguished using dealer id
    stock_no = scrapy.Field() # Stock number assigned to the vehicle by the dealer.
    vin = scrapy.Field() # 17 character vehicle identification number.
    condition = scrapy.Field() # Vehicle condition. Values are : New or Used
    year = scrapy.Field()