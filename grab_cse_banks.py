import os
import argparse

from data_grab.run_scraper_banks_cse import Scraper
from helper.get_proxy import refresh_proxy

parser = argparse.ArgumentParser()

parser.add_argument('-p', '--proxy', help="use proxy", action='store_true')

args = parser.parse_args()

bank_list = ['ABBANK',
             'ALARABANK',
             'BANKASIA',
             'BRACBANK',
             'DHAKABANK',
             'DUTCHBANGL',
             'EBL',
             'EXIMBANK',
             'FIRSTSBANK',
             'GIB',
             'IFIC',
             'ISLAMIBANK',
             'JAMUNABANK',
             'MERCANBANK',
             'MIDLANDBNK',
             'MTB',
             'NCCBANK',
             'NBL',
             'NRBCBANK',
             'ONEBANKLTD',
             'PRIMEBANK',
             'PUBALIBANK',
             'RUPALIBANK',
             'SHAHJABANK',
             'SIBL',
             'SBACBANK',
             'SOUTHEASTB',
             'STANDBANKL',
             'CITYBANK',
             'PREMIERBAN',
             'TRUSTBANK',
             'UNIONBANK',
             'UCB',
             'UTTARABANK']

if args.proxy:
    print("getting proxy IP .. ")
    refresh_proxy()

print("Starting .. ")
scraper = Scraper()
scraper.run_spiders(args.proxy, bank_list)
