# import os
import argparse

from data_grab.run_scraper_top import Scraper
from helper.get_proxy import refresh_proxy

parser = argparse.ArgumentParser()

parser.add_argument('-p', '--proxy', help="use proxy", action='store_true')

args = parser.parse_args()

# if os.path.exists("db/output/top_listing.csv"):
#     os.remove("db/output/top_listing.csv")
#     print("Previous data removed..")
# else:
#     print("No previous data exist..")

if args.proxy:
    print("getting proxy IP .. ")
    refresh_proxy()

print("Starting .. ")
scraper = Scraper()
scraper.run_spiders(args.proxy)
