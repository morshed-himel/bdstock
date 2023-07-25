# Target Data Get

python3 grab_dse_banks.py
python3 grab_cse_banks.py

## Process

# if using virtual env

- python3 -m venv env
- source env/bin/activate

## Dependency

pip or pip3

- pip3 install requests
- pip3 install Scrapy
- pip3 install scrapy-useragents
- pip3 install scrapy-rotating-proxies
- pip3 install mysql-connector-python

- pip install requests
- pip install Scrapy
- pip install scrapy-useragents
- pip install scrapy-rotating-proxies
- pip install mysql-connector-python

## Todo

- connect DB if needed

## Mysql

ssh -i bastion.pem ubuntu@34.234.172.91
http://34.234.172.91/?username=root&db=cardb&table=cars_db
CarData-1

$ sudo chmod 600 /path/to/my/key.pem

ssh -i morshed.pem ubuntu@34.234.172.91

systemctl status mysql.service
sudo systemctl start mysql
sudo systemctl stop mysql

## shell TEST

$ scrapy shell
$ fetch("https://www.kijiji.ca/v-cars-trucks/edmonton/2003-nissan-altima/1519772294")
$ view(response)
$ response.css('.price\_\_detail-price--old del').extract_first()
$ response.xpath('//\*[contains(concat( " ", @class, " " ), concat( " ", "org", " " ))]')

## shell TEST

from scrapy.shell import inspect_response
inspect_response(response, self)
