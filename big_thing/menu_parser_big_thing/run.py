#!/bin/python

from big_thing_py.big_thing import *

import argparse
import requests
import re
from bs4 import BeautifulSoup


def get_menu(url):
    response = requests.get(url)
    today_whole_menu = {}
    tomorrow_whole_menu = {}

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        today_menu_list = soup.select_one(
            '#main > table:nth-child(2)').select('tr')
        tomorrow_menu_list = soup.select_one(
            '#main > table:nth-child(5)').select('tr')

        key = None
        for menu in today_menu_list:
            try:
                if menu.has_attr('height'):
                    key = menu.text
                    today_whole_menu[key] = []
                else:
                    today_whole_menu[key].append((menu.text.split()[0], re.sub(
                        '\d', ' ', ''.join(menu.text.split()[1:])).split()))
            except KeyError:
                pass

        key = None
        for menu in tomorrow_menu_list:
            try:
                if menu.has_attr('height'):
                    key = menu.text
                    tomorrow_whole_menu[key] = []
                else:
                    tomorrow_whole_menu[key].append((menu.text.split()[0], re.sub(
                        '\d', ' ', ''.join(menu.text.split()[1:])).split()))
            except KeyError:
                pass

    return today_whole_menu, tomorrow_whole_menu


def dinner_menu():
    today_whole_menu, tomorrow_whole_menu = get_menu(
        'https://mini.snu.kr/cafe/')
    text = '\n'

    if today_whole_menu.get('저녁', None) == None:
        return '너무 늦어서 저녁 메뉴가 없어요...'
    else:
        dinner_menu = today_whole_menu.get('저녁', None)
        for menu in dinner_menu:
            tmp = "\n".join(menu[1])
            text += f'=== {menu[0]} ===\n{tmp}'

    return text


def lunch_menu():
    today_whole_menu, tomorrow_whole_menu = get_menu(
        'https://mini.snu.kr/cafe/')
    text = '\n'

    if today_whole_menu.get('점심', None) == None:
        return '너무 늦어서 점심 메뉴가 없어요...'
    else:
        lunch_menu = today_whole_menu.get('점심', None)
        for menu in lunch_menu:
            tmp = "\n".join(menu[1])
            text += f'=== {menu[0]} ===\n{tmp}'

    return text


def breakfast_menu():
    pass


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", '-n', action='store', type=str,
                        required=False, default='basic_thing', help="thing name")
    parser.add_argument("--host", '-ip', action='store', type=str,
                        required=False, default='127.0.0.1', help="host name")
    parser.add_argument("--port", '-p', action='store', type=int,
                        required=False, default=1883, help="port")
    parser.add_argument("--alive_cycle", '-ac', action='store', type=int,
                        required=False, default=60, help="alive cycle")
    parser.add_argument("--auto_scan", '-as', action='store_true',
                        required=False, help="middleware auto scan enable")
    parser.add_argument("--log", action='store_true',
                        required=False, help="log enable")
    args, unknown = parser.parse_known_args()

    return args


def generate_thing(args):
    tag_list = [SoPTag(name='menu')]
    function_list = [SoPFunction(func=lunch_menu,
                                 return_type=SoPType.STRING,
                                 tag_list=tag_list,
                                 arg_list=[]),
                     SoPFunction(func=dinner_menu,
                                 return_type=SoPType.STRING,
                                 tag_list=tag_list,
                                 arg_list=[])]
    value_list = []

    thing = SoPBigThing(name=args.name, ip=args.host, port=args.port, alive_cycle=args.alive_cycle,
                        service_list=function_list + value_list)
    return thing


if __name__ == '__main__':

    args = arg_parse()
    thing = generate_thing(args)
    thing.setup(avahi_enable=args.auto_scan)
    thing.run()
