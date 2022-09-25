#!/bin/python


from big_thing_py.big_thing import *
from timelapse_utils import *

import argparse


timelapse = Timelapse()


# @static_vars(flag=False, start_time=0)
# def sense_time_passed():
#     if not sense_time_passed.flag:
#         sense_time_passed.flag = True
#         sense_time_passed.start_time = time.time()
#     return time.time() - sense_time_passed.start_time


# def sense_capture_picture_num():
#     return timelapse.capture_num


def actuate_timelapse_start() -> bool:
    timelapse.start_capture()
    return True


def actuate_timelapse_stop() -> bool:
    timelapse.stop_capture()
    return True


def actuate_timelapse_makevideo() -> bool:
    result = timelapse.make_video()
    return result


def arg_parse():
    parser = argparse.ArgumentParser()
    # parser.add_argument("--log", action='store_true', dest='log',
    #                     required=False, default=True, help="make log file")
    parser.add_argument("--name", '-n', action='store',
                        required=False, default='TestSuperClient', help="client name")
    parser.add_argument("--host", '-ip', action='store',
                        required=False, default='192.168.50.181', help="host name")
    parser.add_argument("--port", '-p', action='store',
                        required=False, default=1883, help="port")
    parser.add_argument("--refresh_cycle", '-rc', action='store',
                        required=False, default=5, help="refresh_cycle")
    args, unknown = parser.parse_known_args()

    return args


def generate_thing(args):
    timelapse.run_thread()
    tag_list = SoPTag(name='timelapse')

    # value_list = [SoPValue(name='time_passed',
    #                        function=sense_time_passed,
    #                        type='int',
    #                        bound=(0, 100),
    #                        tag_list=[timelapse_tag, ],
    #                        cycle=1),
    #               SoPValue(name='capture_picture_num',
    #                        function=sense_capture_picture_num,
    #                        type='int',
    #                        bound=(0, 100),
    #                        tag_list=[timelapse_tag, ],
    #                        cycle=1)]
    value_list = []
    function_list = [SoPFunction(name='timelapse_start',
                                 func=actuate_timelapse_start,
                                 return_type=SoPType.BOOL,
                                 tag_list=tag_list,
                                 arg_list=[]),
                     SoPFunction(name='timelapse_stop',
                                 func=actuate_timelapse_stop,
                                 return_type=SoPType.BOOL,
                                 tag_list=tag_list,
                                 arg_list=[]),
                     SoPFunction(name='timelapse_makevideo',
                                 func=actuate_timelapse_makevideo,
                                 return_type=SoPType.BOOL,
                                 tag_list=tag_list,
                                 arg_list=[])]

    thing = SoPBigThing(name=args.name, ip=args.host, port=args.port, alive_cycle=args.alive_cycle,
                        service_list=function_list + value_list)
    return thing


def main():
    thing = generate_thing(arg_parse())
    thing.setup(avahi_enable=False)
    thing.run()


if __name__ == '__main__':
    main()
