#!/bin/python3

from big_thing_py.big_thing import *

import argparse
import os


def human_num():
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
    # parser.add_argument("--log", action='store_true', dest='log',
    #                     required=False, default=True, help="make log file")
    parser.add_argument("--name", '-n', action='store',
                        required=False, default='TestSuperClient', help="client name")
    parser.add_argument("--host", '-ip', action='store',
                        required=False, default='147.46.114.165', help="host name")
    parser.add_argument("--port", '-p', action='store',
                        required=False, default=22283, help="port")
    parser.add_argument("--refresh_cycle", '-rc', action='store',
                        required=False, default=5, help="refresh_cycle")
    args, unknown = parser.parse_known_args()

    return args


def run_object_detector():
    os.system("./backend_run.sh > /dev/null 2>&1 &")


def main():
    args = arg_parse()

    tag1 = SoPTag(name='human_detector')
    tag2 = SoPTag(name='camera')
    tag_list = [tag1, tag2]

    function_list = []

    value1 = SoPValue(name='human_num',
                      func=human_num,
                      type=SoPType.INTEGER,
                      bound=(0, 10000),
                      tag_list=tag_list,
                      cycle=10)
    value_list = [value1]

    service_list = function_list + value_list

    thing = SoPBigThing(name='human_detector', service_list=service_list,
                        alive_cycle=10, is_super=False, is_parallel=True, ip='147.46.114.165', port=22183,
                        ssl_ca_path=f'{get_project_root()}/CA/', ssl_enable=None)

    # run_object_detector()
    thing.setup(avahi_enable=False)
    thing.run()


if __name__ == '__main__':
    main()
