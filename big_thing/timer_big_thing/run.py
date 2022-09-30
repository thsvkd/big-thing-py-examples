#!/bin/python

from big_thing_py.big_thing import *

import argparse
import time


class SoPTimer():
    def __init__(self, timeout: float = None) -> None:
        self.timeout = timeout
        self.is_set = False
        self.timer_thread = None

    def timer_start(self) -> bool:
        Thread(target=self.timeout_thread_func).start()
        return True

    def set_timer(self, timeout: float) -> float:
        self.timeout = float(timeout)
        self.is_set = False
        return self.timeout

    def timeout_thread_func(self) -> None:
        print('timer started')
        time.sleep(self.timeout)
        self.is_set = True
        print('timer ended')


timer = SoPTimer()


def is_set() -> float:
    global timer
    return timer.is_set


def start() -> bool:
    global timer
    return timer.timer_start()


def reset(timeout: float) -> float:
    global timer
    return timer.set_timer(timeout)


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", '-n', action='store', type=str,
                        required=False, default='timer_big_thing', help="thing name")
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
    tag_list = [SoPTag(name='clock')]
    value_list = [SoPValue(func=is_set,
                           type=SoPType.BOOL,
                           bound=(0, 2),
                           cycle=0.1,
                           tag_list=tag_list)]
    function_list = [SoPFunction(func=start,
                                 return_type=SoPType.BOOL,
                                 tag_list=tag_list,
                                 arg_list=[]),
                     SoPFunction(func=reset,
                                 return_type=SoPType.BOOL,
                                 tag_list=tag_list,
                                 arg_list=[SoPArgument(name='timeout_arg',
                                                       type=SoPType.DOUBLE,
                                                       bound=(0, 1000000))])]

    thing = SoPBigThing(name=args.name, ip=args.host, port=args.port, alive_cycle=args.alive_cycle,
                        service_list=function_list + value_list)
    return thing


if __name__ == '__main__':
    args = arg_parse()
    thing = generate_thing(args)
    thing.setup(avahi_enable=args.auto_scan)
    thing.run()
