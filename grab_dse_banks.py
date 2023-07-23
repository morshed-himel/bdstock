import os
import argparse

from data_grab.run_scraper_banks_dse import Scraper
from helper.get_proxy import refresh_proxy

parser = argparse.ArgumentParser()

parser.add_argument('-p', '--proxy', help="use proxy", action='store_true')

args = parser.parse_args()

# bank_list = ['ABBANK', 'ALARABANK', 'BANKASIA']
bank_list = ['ABBANK', 'ALARABANK', 'BANKASIA', 'BRACBANK', 'CITYBANK', 'DHAKABANK', 'DUTCHBANGL', 'EBL', 'EXIMBANK', 'FIRSTSBANK', 'GIB', 'ICBIBANK', 'IFIC', 'ISLAMIBANK', 'JAMUNABANK', 'MERCANBANK', 'MTB',
             'NBL', 'NCCBANK', 'NRBCBANK', 'ONEBANKLTD', 'PREMIERBAN', 'PRIMEBANK', 'PUBALIBANK', 'RUPALIBANK', 'SBACBANK', 'SHAHJABANK', 'SIBL', 'SOUTHEASTB', 'STANDBANKL', 'TRUSTBANK', 'UCB', 'UNIONBANK', 'UTTARABANK']


if args.proxy:
    print("getting proxy IP .. ")
    refresh_proxy()

print("Starting .. ")
scraper = Scraper()
scraper.run_spiders(args.proxy, bank_list)
