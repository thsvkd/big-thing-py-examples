#!/bin/python

from big_thing_py.big_thing import *
from big_thing_py.utils.api_util import *

import argparse


kakao_apiclient = NaverAPIClient('')


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
    tag_list = [SoPTag(name='kakao')]
    function_list = [SoPFunction(func=kakao_search,
                                 return_type=SoPType.STRING,
                                 tag_list=tag_list,
                                 arg_list=[SoPArgument(name='text_arg',
                                                       type=SoPType.STRING,
                                                       bound=(0, 10000))]),
                     SoPFunction(func=kakao_pose,
                                 return_type=SoPType.STRING,
                                 tag_list=tag_list,
                                 arg_list=[SoPArgument(name='image_path_arg',
                                                       type=SoPType.STRING,
                                                       bound=(0, 10000))]),
                     SoPFunction(func=kakao_OCR,
                                 return_type=SoPType.STRING,
                                 tag_list=tag_list,
                                 arg_list=[SoPArgument(name='image_path_arg',
                                                       type=SoPType.STRING,
                                                       bound=(0, 10000))]),
                     SoPFunction(func=kakao_translation,
                                 return_type=SoPType.STRING,
                                 tag_list=tag_list,
                                 arg_list=[SoPArgument(name='text_arg',
                                                       type=SoPType.STRING,
                                                       bound=(0, 10000))])]
    value_list = []

    thing = SoPBigThing(name=args.name, ip=args.host, port=args.port, alive_cycle=args.alive_cycle,
                        service_list=function_list + value_list)
    return thing


if __name__ == '__main__':
    args = arg_parse()
    thing = generate_thing(args)
    thing.setup(avahi_enable=args.auto_scan)
    thing.run()
