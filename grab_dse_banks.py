import json
import argparse

from data_grab.run_scraper_dse import Scraper
from helper.get_proxy import refresh_proxy
from config import JSON_PATH_DSE_LISTING


def find_index_in_json_array(json_array, search_text, key):
    for index, item in enumerate(json_array):
        if item.get(key) == search_text:
            return index
    return -1


bank_list = []

with open(JSON_PATH_DSE_LISTING, 'r') as file:
    json_array = json.load(file)

    search_text = "Bank"
    key_to_search = "category_name"
    index = find_index_in_json_array(json_array, search_text, key_to_search)

    if index != -1:
        bank_list = json_array[index]["catalog"]
    else:
        print(f"'{search_text}' not found in the {JSON_PATH_DSE_LISTING}")

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--proxy', help="use proxy", action='store_true')
args = parser.parse_args()


if args.proxy:
    print("getting proxy IP .. ")
    refresh_proxy()

print("Starting .. ")
scraper = Scraper()
scraper.run_spiders(args.proxy, bank_list)
