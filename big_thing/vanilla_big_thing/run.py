from big_thing_py.big_thing import *

import time
import random
import argparse


def function_dummy_no_arg() -> int:
    print('function_dummy_no_arg run... return 1')
    return 1


def function_dummy_with_arg(int_arg: int, float_arg: float, str_arg: str, bool_arg: bool) -> bool:
    try:
        print('function_dummy_with_arg start')
        print('int_arg : ', int_arg)
        print('float_arg : ', float_arg)
        print('str_arg : ', str_arg)
        print('bool_arg : ', bool_arg)
    except Exception as e:
        print_error(e)
        return False
    else:
        return True


def function_dummy_with_arg_and_delay(int_arg: int, float_arg: float, str_arg: str, bool_arg: bool) -> bool:
    print('function_dummy_with_arg_and_delay run')
    function_dummy_with_arg(int_arg, float_arg, str_arg, bool_arg)

    for i in range(10):
        SOPLOG_DEBUG(f'deley : {i}')
        time.sleep(1)

    return True


def value_dummy():
    print('value_dummy run! current time : ')
    return int(get_current_time())


def arg_parse():
    parser = argparse.ArgumentParser()
    # parser.add_argument("--log", action='store_true', dest='log',
    #                     required=False, default=True, help="make log file")
    parser.add_argument("--name", '-n', action='store', type=str,
                        required=False, default='vallina_thing', help="client name")
    parser.add_argument("--host", '-ip', action='store', type=str,
                        required=False, default='127.0.0.1', help="host name")
    parser.add_argument("--port", '-p', action='store', type=int,
                        required=False, default=1883, help="port")
    parser.add_argument("--alive_cycle", '-ac', action='store',
                        required=False, default=60, help="alive cycle")
    parser.add_argument("--refresh_cycle", '-rc', action='store',
                        required=False, default=5, help="refresh cycle")
    args, unknown = parser.parse_known_args()

    return args


def main():
    args = arg_parse()

    tag1 = SoPTag(name='tag1')
    tag_list = [tag1]

    int_arg = SoPArgument(name='int_arg',
                          type=SoPType.INTEGER,
                          bound=(0, 10000))
    float_arg = SoPArgument(name='float_arg',
                            type=SoPType.DOUBLE,  # float
                            bound=(0, 10000))
    str_arg = SoPArgument(name='str_arg',
                          type=SoPType.STRING,
                          bound=(0, 10000))
    bool_arg = SoPArgument(name='bool_arg',
                           type=SoPType.BOOL,
                           bound=(0, 10000))
    arg_list = [int_arg, float_arg, str_arg, bool_arg]

    func1 = SoPFunction(name='function_dummy_no_arg',
                        func=function_dummy_no_arg,
                        return_type=SoPType.INTEGER,
                        tag_list=tag_list,
                        arg_list=[],
                        energy=45)
    func2 = SoPFunction(name='function_dummy_with_arg',
                        func=function_dummy_with_arg,
                        return_type=SoPType.INTEGER,
                        tag_list=tag_list,
                        arg_list=arg_list,
                        energy=12)
    func3 = SoPFunction(name='function_dummy_with_arg_and_delay',
                        func=function_dummy_with_arg_and_delay,
                        return_type=SoPType.INTEGER,
                        timeout=5,
                        tag_list=tag_list,
                        arg_list=arg_list,
                        energy=56)
    function_list = [func1, func2, func3, ]

    value1 = SoPValue(name='time',
                      func=value_dummy,
                      type=SoPType.INTEGER,
                      bound=(0, 99999999999),
                      tag_list=tag_list,
                      cycle=10)
    value_list = [value1]

    service_list = function_list + value_list

    thing = SoPBigThing(name=args.name, service_list=service_list,
                        alive_cycle=10, is_super=False, is_parallel=True, ip=args.host, port=args.port)

    thing.setup(avahi_enable=False)
    thing.run()


if __name__ == '__main__':
    main()
