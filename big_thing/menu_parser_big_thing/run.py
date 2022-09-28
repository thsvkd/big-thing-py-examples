#!/bin/python

from big_thing_py.big_thing import *

import argparse
import os


def dinner_menu():
    os.system(f'node parse.js 0')
    with open('menu.txt', 'r') as f:
        return ''.join(f.readlines())


def lunch_menu():
    os.system(f'node parse.js 1')
    with open('menu.txt', 'r') as f:
        return ''.join(f.readlines())


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
