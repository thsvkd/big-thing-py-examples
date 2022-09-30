#!/bin/python3

from big_thing_py.big_thing import *

import argparse
import os


def run_object_detector():
    os.system("./backend_run.sh > /dev/null 2>&1 &")


def human_num() -> int:
    object_data = json_file_read('obj.json')
    if object_data:
        object_list = object_data['obj']
    else:
        return 0

    human_num = 0
    for object in object_list:
        if object['ClassID'] == 1:
            human_num += 1

    return human_num


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", '-n', action='store', type=str,
                        required=False, default='human_detector_big_thing', help="thing name")
    parser.add_argument("--host", '-ip', action='store', type=str,
                        required=False, default='127.0.0.1', help="host name")
    parser.add_argument("--port", '-p', action='store', type=int,
                        required=False, default=1883, help="port")
    parser.add_argument("--alive_cycle", '-ac', action='store', type=int,
                        required=False, default=60, help="alive cycle")
    parser.add_argument("--log", action='store_true', dest='log',
                        required=False, default=True, help="log enable")
    args, unknown = parser.parse_known_args()

    return args


def generate_thing(args):
    args = arg_parse()
    tag_list = [SoPTag(name='human_detector'),
                SoPTag(name='camera')]

    function_list = []
    value_list = [SoPValue(name='human_num',
                           func=human_num,
                           type=SoPType.INTEGER,
                           bound=(0, 10000),
                           tag_list=tag_list,
                           cycle=10)]

    thing = SoPBigThing(name=args.name, ip=args.host, port=args.port, alive_cycle=args.alive_cycle,
                        service_list=function_list + value_list)
    return thing


if __name__ == '__main__':
    run_object_detector()
    args = arg_parse()
    thing = generate_thing(args)
    thing.setup(avahi_enable=args.auto_scan)
    thing.run()
