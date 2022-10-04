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


def actuate_timelapse_makevideo(dst: str = './video_out') -> bool:
    result = timelapse.make_video(des_path=dst)
    return result


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", '-n', action='store', type=str,
                        required=False, default='timelapse_big_thing', help="thing name")
    parser.add_argument("--host", '-ip', action='store', type=str,
                        required=False, default='127.0.0.1', help="host name")
    parser.add_argument("--port", '-p', action='store', type=int,
                        required=False, default=11083, help="port")
    parser.add_argument("--alive_cycle", '-ac', action='store', type=int,
                        required=False, default=60, help="alive cycle")
    parser.add_argument("--auto_scan", '-as', action='store_true',
                        required=False, help="middleware auto scan enable")
    parser.add_argument("--log", action='store_true',
                        required=False, help="log enable")
    args, unknown = parser.parse_known_args()

    return args


def generate_thing(args):
    timelapse.run_thread()
    tag_list = [SoPTag(name='timelapse')]

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
                                 arg_list=[SoPArgument(name='video_out_path',
                                                       bound=(0, 1000),
                                                       type=SoPType.STRING)])]

    thing = SoPBigThing(name=args.name, ip=args.host, port=args.port, alive_cycle=args.alive_cycle,
                        service_list=function_list + value_list)
    return thing


if __name__ == '__main__':
    args = arg_parse()
    thing = generate_thing(args)
    thing.setup(avahi_enable=args.auto_scan)
    thing.run()
