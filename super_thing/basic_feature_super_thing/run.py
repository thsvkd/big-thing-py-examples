#!/bin/python

from big_thing_py.super_thing import *

import argparse


class SoPBasicSuperThing(SoPSuperThing):

    def __init__(self, name: str = None, service_list: List[SoPService] = [], alive_cycle: float = 60, is_super: bool = False, is_parallel: bool = True,
                 ip: str = None, port: int = None, ssl_ca_path: str = None, ssl_enable: bool = None, refresh_cycle: float = 10):
        super().__init__(name=name, service_list=service_list, alive_cycle=alive_cycle, is_super=is_super,
                         is_parallel=is_parallel, ip=ip, port=port, ssl_ca_path=ssl_ca_path, ssl_enable=ssl_enable, refresh_cycle=refresh_cycle)

        tag_list = [SoPTag(name='super'),
                    SoPTag(name='basic'),
                    SoPTag(name='big_thing'),
                    SoPTag(name='function')]
        arg_list = []

        self._value_list = []
        self._function_list = [SoPSuperFunction(func=self.super_func_execute_func_no_arg_SINGLE,
                                                return_type=SoPType.INTEGER,
                                                tag_list=tag_list,
                                                arg_list=arg_list,
                                                energy=110),
                               SoPSuperFunction(func=self.super_func_execute_func_no_arg_ALL,
                                                return_type=SoPType.INTEGER,
                                                tag_list=tag_list,
                                                arg_list=arg_list,
                                                energy=110),
                               SoPSuperFunction(func=self.super_func_get_value_current_time_SINGLE,
                                                return_type=SoPType.INTEGER,
                                                tag_list=tag_list,
                                                arg_list=arg_list,
                                                energy=110),
                               SoPSuperFunction(func=self.super_func_get_value_current_time_ALL,
                                                return_type=SoPType.INTEGER,
                                                tag_list=tag_list,
                                                arg_list=arg_list,
                                                energy=110)]

        self._is_super = True

    def super_func_execute_func_no_arg_SINGLE(self) -> int:
        result_list = self.req(service_name='func_no_arg',
                               service_type=SoPServiceType.FUNCTION, policy=SoPPolicy.SINGLE)

        result_sum = 0
        if result_list:
            for result in result_list:
                result_sum += result['return_value']

            return result_sum
        else:
            return 0

    def super_func_execute_func_no_arg_ALL(self) -> int:
        result_list = self.req(service_name='func_no_arg',
                               service_type=SoPServiceType.FUNCTION, policy=SoPPolicy.ALL)

        result_sum = 0
        if result_list:
            for result in result_list:
                result_sum += result['return_value']

            return result_sum
        else:
            return 0

    def super_func_get_value_current_time_SINGLE(self) -> int:
        result_list = self.req(service_name='value_current_time',
                               service_type=SoPServiceType.VALUE, policy=SoPPolicy.SINGLE)

        result_sum = 0
        if result_list:
            for result in result_list:
                result_sum += result['return_value']

            return result_sum
        else:
            return 0

    def super_func_get_value_current_time_ALL(self) -> int:
        result_list = self.req(service_name='value_current_time',
                               service_type=SoPServiceType.VALUE, policy=SoPPolicy.ALL)

        result_sum = 0
        if result_list:
            for result in result_list:
                result_sum += result['return_value']

            return result_sum
        else:
            return 0

    # def super_func_req_scenario_line(self, scenario_line: str) -> bool:
    #     result_list = self.r(scenario_line)
    #     # result_list = self.r('(#Hue).on()')
    #     # result_list = self.r('(#Hue).set_brightness($1)', 100)
    #     # result_list = self.r('(#Hue).off()')

    #     return result_list


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", '-n', action='store', type=str,
                        required=False, default='basic_thing', help="thing name")
    parser.add_argument("--host", '-ip', action='store', type=str,
                        required=False, default='127.0.0.1', help="host name")
    parser.add_argument("--port", '-p', action='store', type=int,
                        required=False, default=11083, help="port")
    parser.add_argument("--alive_cycle", '-ac', action='store', type=int,
                        required=False, default=60, help="alive cycle")
    parser.add_argument("--refresh_cycle", '-rc', action='store', type=int,
                        required=False, default=60, help="refresh cycle")
    parser.add_argument("--log", action='store_true', dest='log',
                        required=False, default=True, help="log enable")
    args, unknown = parser.parse_known_args()

    return args


def main():
    args = arg_parse()
    super_thing = SoPBasicSuperThing(name=args.name, ip=args.host, port=args.port, alive_cycle=args.alive_cycle,
                                     refresh_cycle=args.refresh_cycle)
    super_thing.setup(avahi_enable=False)
    super_thing.run()


if __name__ == '__main__':
    main()
