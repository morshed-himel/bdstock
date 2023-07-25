import os
import sys
import json
import argparse
import subprocess


from data_grab.run_scraper_dse import Scraper
from helper.get_proxy import refresh_proxy
from config import JSON_PATH_DSE_LISTING


def find_index_in_json_array(json_array, search_text, key):
    for index, item in enumerate(json_array):
        if item.get(key) == search_text:
            return index
    return -1


def get_all_code():
    completed_process = subprocess.run(
        ['python', 'grab_dse_listing.py'], capture_output=True, text=True)

    if completed_process.returncode == 0:
        print("All code grab successfully from DSE.")
    else:
        print("DSE data grab execution failed. Exiting")
        sys.exit()


def get_list_for_category(category):
    with open(JSON_PATH_DSE_LISTING, 'r') as file:
        json_array = json.load(file)

        key_to_search = "category_name"
        index = find_index_in_json_array(json_array, category, key_to_search)

        if index != -1:
            return json_array[index]["catalog"]
        else:
            print(f"'{category}' not found in the {JSON_PATH_DSE_LISTING}")
            sys.exit()


def get_full_list():
    with open(JSON_PATH_DSE_LISTING, 'r') as file:
        return json.load(file)


scraper = Scraper()
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--proxy', help="use proxy", action='store_true')
parser.add_argument('-a', '--all', help="get all category",
                    action='store_true')
args = parser.parse_args()

if not os.path.exists(JSON_PATH_DSE_LISTING):
    print("DSE Listing not found. Getting new data")
    get_all_code()

if args.proxy:
    print("getting proxy IP .. ")
    refresh_proxy()

if args.all:
    print("Getting All Category. .... ")
    category = "All"
    scraper.run_to_get_all(args.proxy, get_full_list())
else:
    print("Getting Banks Only. Starting .. ")
    category = "Bank"
    bank_list = get_list_for_category(category)
    scraper.run_spiders(args.proxy, category, bank_list)
