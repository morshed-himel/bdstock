import scrapy

class CarItem(scrapy.Item):
    dealer_id = scrapy.Field() # Dealer Id identifier for composite feed, dealer inventory feed can be distinguished using dealer id
    stock_no = scrapy.Field() # Stock number assigned to the vehicle by the dealer.
    vin = scrapy.Field() # 17 character vehicle identification number.
    condition = scrapy.Field() # Vehicle condition. Values are : New or Used
    year = scrapy.Field()
    make = scrapy.Field()
    model = scrapy.Field()
    trim = scrapy.Field()
    body = scrapy.Field() # Body Style.
    odometer = scrapy.Field()
    retail = scrapy.Field() # Dealer retail price, Base Price
    sale = scrapy.Field() # Dealer sales price.
    sold = scrapy.Field() # Dealer sold price.
    description = scrapy.Field()
    doors = scrapy.Field() # Number of doors.
    passengers = scrapy.Field() # Number of Passenger.
    fueltype = scrapy.Field() #Fuel type. Gas, Diesel, Electric, Hybrid, Flexible
    engine = scrapy.Field() # Engine - e.g. 4 Cyl 2.0L
    drivetrain = scrapy.Field() # Drivetrain - e.g. FWD, RWD, AWD
    transmission = scrapy.Field() # Transmission, values are Automatic, Manual, CVT
    
    color_int = scrapy.Field() # Interior Color of the vehicle.
    color_ext = scrapy.Field() # Exterior Color of the vehicle.
    economy_city = scrapy.Field() # City Fuel Economy
    economy_hwy = scrapy.Field() # Highway Fuel Economy
    
    images = scrapy.Field() # Vehicle Images
    url = scrapy.Field() # Dealer’s vehicle details page URL

    #####################

    latitude = scrapy.Field()
    longitude = scrapy.Field()
    
    city = scrapy.Field()
    province = scrapy.Field()
    
    address = scrapy.Field()

    #####################

    title = scrapy.Field()
    scrap_date = scrapy.Field() 
    post_date = scrapy.Field()