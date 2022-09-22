from big_thing_py.big_thing import *

import random
import argparse


def float_function_no_arg() -> float:
    ran_float = random.uniform(0, 100)
    SOPLOG_DEBUG(
        f'{get_current_function_name()} run. return {ran_float}', 'green')
    return ran_float


def str_function_no_arg() -> str:
    test_string = 'test_string'
    SOPLOG_DEBUG(
        f'{get_current_function_name()} run. return {test_string}', 'green')
    return test_string


def float_function_with_arg(int_arg: int, float_arg: float, str_arg: str, bool_arg: bool, ) -> float:
    ran_float = random.uniform(0, 100)
    SOPLOG_DEBUG(f'{get_current_function_name()} run', 'green')
    SOPLOG_DEBUG(f'int_arg : {int_arg}', 'yellow')
    SOPLOG_DEBUG(f'float_arg : {float_arg}', 'yellow')
    SOPLOG_DEBUG(f'str_arg : {str_arg}', 'yellow')
    SOPLOG_DEBUG(f'bool_arg : {bool_arg}', 'yellow')
    # SOPLOG_DEBUG(f'binary_arg : {binary_arg}', 'yellow')
    SOPLOG_DEBUG(
        f'{get_current_function_name()} end. return {ran_float}', 'green')
    return ran_float


def str_function_with_arg(int_arg: int, float_arg: float, str_arg: str, bool_arg: bool, ) -> str:
    test_string = 'test_string'
    SOPLOG_DEBUG(f'{get_current_function_name()} run', 'green')
    SOPLOG_DEBUG(f'int_arg : {int_arg}', 'yellow')
    SOPLOG_DEBUG(f'float_arg : {float_arg}', 'yellow')
    SOPLOG_DEBUG(f'str_arg : {str_arg}', 'yellow')
    SOPLOG_DEBUG(f'bool_arg : {bool_arg}', 'yellow')
    # SOPLOG_DEBUG(f'binary_arg : {binary_arg}', 'yellow')
    SOPLOG_DEBUG(
        f'{get_current_function_name()} end. return {test_string}', 'green')
    return f'{test_string} {int_arg} {float_arg} {str_arg} {bool_arg}'


def gen_test_thing() -> SoPBigThing:
    alive_cycle = 1
    value_cycle = alive_cycle

    tag_list = [SoPTag('normal_string1'),
                SoPTag('normal_string2'),
                SoPTag('-+_()*&^%$#@!~`=><')]

    arg_list = [SoPArgument(name='int_arg',
                            type=SoPType.INTEGER,
                            bound=(-2147483648, 2147483647)),
                SoPArgument(name='float_arg',
                            type=SoPType.DOUBLE,
                            bound=(-2147483648, 2147483647)),
                SoPArgument(name='str_arg',
                            type=SoPType.STRING,
                            bound=(-2147483648, 2147483647)),
                SoPArgument(name='bool_arg',
                            type=SoPType.BOOL,
                            bound=(-2147483648, 2147483647)),
                ]

    value_list = [
        SoPValue(name='float_function_no_arg',
                 func=float_function_no_arg,
                 type=SoPType.DOUBLE,
                 bound=(-2147483648, 2147483647),
                 tag_list=tag_list,
                 cycle=value_cycle),
        SoPValue(name='str_function_no_arg',
                 func=str_function_no_arg,
                 type=SoPType.STRING,
                 bound=(-2147483648, 2147483647),
                 tag_list=tag_list,
                 cycle=value_cycle),
    ]

    no_arg_function_list = [
        SoPFunction(name='float_function_no_arg',
                    func=float_function_no_arg,
                    return_type=SoPType.DOUBLE,
                    desc='float_function_no_arg',
                    tag_list=tag_list,
                    arg_list=[],
                    exec_time=1000 * 10,
                    timeout=1000 * 10,
                    policy=SoPPolicy.SINGLE),
        SoPFunction(name='str_function_no_arg',
                    func=str_function_no_arg,
                    return_type=SoPType.STRING,
                    desc='str_function_no_arg',
                    tag_list=tag_list,
                    arg_list=[],
                    exec_time=1000 * 10,
                    timeout=1000 * 10,
                    policy=SoPPolicy.SINGLE),
    ]
    arg_function_list = [
        SoPFunction(name='float_function_with_arg',
                    func=float_function_with_arg,
                    return_type=SoPType.DOUBLE,
                    desc='float_function_with_arg',
                    tag_list=tag_list,
                    arg_list=arg_list,
                    exec_time=1000 * 10,
                    timeout=1000 * 10,
                    policy=SoPPolicy.SINGLE),
        SoPFunction(name='str_function_with_arg',
                    func=str_function_with_arg,
                    return_type=SoPType.STRING,
                    desc='str_function_with_arg',
                    tag_list=tag_list,
                    arg_list=arg_list,
                    exec_time=1000 * 10,
                    timeout=1000 * 10,
                    policy=SoPPolicy.SINGLE),
    ]
    service_list = value_list + no_arg_function_list + arg_function_list

    thing = SoPBigThing(name='BigThingTest', service_list=service_list,
                        alive_cycle=alive_cycle, is_super=False, is_parallel=True, ip='127.0.0.1', port=1883,
                        ssl_ca_path=f'{get_project_root()}/CA/', ssl_enable=None)

    return thing


def main():
    thing = gen_test_thing()

    thing.setup(avahi_enable=False)
    thing.run()


if __name__ == '__main__':
    main()
