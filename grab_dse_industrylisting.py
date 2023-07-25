import os
import argparse

from data_grab.run_scraper_dse import Scraper
from helper.get_proxy import refresh_proxy
from config import JSON_PATH_DSE_LISTING


def delete_file_if_exists(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"File '{file_path}' deleted successfully.")
    else:
        print(f"File '{file_path}' does not exist.")


delete_file_if_exists(JSON_PATH_DSE_LISTING)

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--proxy', help="use proxy", action='store_true')

args = parser.parse_args()

if args.proxy:
    print("getting proxy IP .. ")
    refresh_proxy()

print("Getting Industry listing.. ")
scraper = Scraper()
scraper.run_spider_listing(args.proxy)
