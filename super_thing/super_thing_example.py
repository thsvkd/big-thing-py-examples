#!/bin/python

from big_thing_py.super_thing import *

import argparse


class SoPLevel1SuperThing(SoPSuperThing):

    def __init__(self, name: str = None, service_list: List[SoPService] = [], alive_cycle: float = 60, is_super: bool = False, is_parallel: bool = True,
                 ip: str = None, port: int = None, ssl_ca_path: str = None, ssl_enable: bool = None, refresh_cycle: float = 10):
        super().__init__(name=name, service_list=service_list, alive_cycle=alive_cycle, is_super=is_super,
                         is_parallel=is_parallel, ip=ip, port=port, ssl_ca_path=ssl_ca_path, ssl_enable=ssl_enable, refresh_cycle=refresh_cycle)

        tag_list = [SoPTag(name='super_thing'), SoPTag(
            name=name + f'_{self._mac_address}')]
        on_all_func = SoPSuperFunction(name=self.on_all.__name__,
                                       func=self.on_all,
                                       return_type=type_converter(
                                           get_function_return_type(self.on_all)),
                                       tag_list=[] + tag_list,
                                       arg_list=[],
                                       timeout=30, exec_time=10)
        off_all_func = SoPSuperFunction(name=self.off_all.__name__,
                                        func=self.off_all,
                                        return_type=type_converter(
                                            get_function_return_type(self.off_all)),
                                        tag_list=[] + tag_list,
                                        arg_list=[],
                                        timeout=30, exec_time=10)

        r_arg = SoPArgument(name='r', type=SoPType.INTEGER, bound=(0, 255))
        g_arg = SoPArgument(name='g', type=SoPType.INTEGER, bound=(0, 255))
        b_arg = SoPArgument(name='b', type=SoPType.INTEGER, bound=(0, 255))
        notify_professor_func = SoPSuperFunction(name=self.notify_professor.__name__,
                                                 func=self.notify_professor,
                                                 return_type=type_converter(
                                                     get_function_return_type(self.notify_professor)),
                                                 tag_list=[] + tag_list,
                                                 arg_list=[
                                                     r_arg, g_arg, b_arg],
                                                 timeout=30, exec_time=10)

        test_request_value_func = SoPSuperFunction(name=self.test_request_value.__name__,
                                                   func=self.test_request_value,
                                                   return_type=type_converter(
                                                       get_function_return_type(self.test_request_value)),
                                                   tag_list=[] + tag_list,
                                                   arg_list=[],
                                                   timeout=30, exec_time=10)

        test_request_line_func = SoPSuperFunction(name=self.test_request_line.__name__,
                                                  func=self.test_request_line,
                                                  return_type=type_converter(
                                                      get_function_return_type(self.test_request_line)),
                                                  tag_list=[] + tag_list,
                                                  arg_list=[],
                                                  timeout=30, exec_time=10)

        super_hue_off_func = SoPSuperFunction(name=self.super_hue_off.__name__,
                                              func=self.super_hue_off,
                                              return_type=type_converter(
                                                  get_function_return_type(self.super_hue_off)),
                                              tag_list=[] + tag_list,
                                              arg_list=[],
                                              timeout=30, exec_time=10)

        self._value_list = []
        self._function_list = [on_all_func,
                               off_all_func,
                               notify_professor_func,
                               test_request_value_func,
                               test_request_line_func,
                               super_hue_off_func]
        self._alive_cycle = 10
        self._is_super = True

    def setup(self, avahi_enable=True):
        return super().setup(avahi_enable=avahi_enable)

    def run(self):
        return super().run()

    def wrapup(self):
        return super().wrapup()

    def handle_result_list(self, result_list):
        if not result_list:
            return result_list
        for result in result_list:
            if result['return_value'] is False:
                return False
        else:
            return True

    # super functions
    def super_hue_off(self) -> bool:
        result_list = self.req(
            service_name='off', service_type=SoPServiceType.FUNCTION, policy=SoPPolicy.SINGLE)
        SoPPolicy.SINGLE
        SoPPolicy.ALL
        return self.handle_result_list(result_list)

    def off_all(self) -> bool:
        result_list = self.req(
            tag_list='Hue', service_name='off', service_type=SoPServiceType.FUNCTION, policy=SoPPolicy.ALL)

        return self.handle_result_list(result_list)

    def on_all(self) -> bool:
        result_list = self.req(
            tag_list='tag1', service_name='on', service_type=SoPServiceType.FUNCTION, policy=SoPPolicy.ALL)

        return self.handle_result_list(result_list)

    def notify_professor(self, r, g, b) -> bool:
        result_list = self.req(tag_list='Hue', service_name='set_color', arg_list=(
            r, g, b), service_type=SoPServiceType.FUNCTION, policy=SoPPolicy.ALL)

        return self.handle_result_list(result_list)

    def test_all(self, r, g, b) -> bool:
        result_list_on = self.req(super_function_name=get_current_function_name(
        ), target_function_name='on', tag_list='Hue')

        print(result_list_on)
        for result in result_list_on:
            if result['return_value'] is False:
                return False

        result_list_set_color = self.req(tag_list='Hue', service_name='set_color', arg_list=(
            r, g, b), service_type=SoPServiceType.FUNCTION, policy=SoPPolicy.ALL)

        print(result_list_set_color)
        for result in result_list_set_color:
            if result['return_value'] is False:
                return False

        result_list_off = self.req(tag_list='Hue', service_name='set_color', arg_list=(
            r, g, b), service_type=SoPServiceType.FUNCTION, policy=SoPPolicy.ALL)

        print(result_list_off)
        for result in result_list_off:
            if result['return_value'] is False:
                return False

    def test_request_value(self) -> bool:
        result_list = self.req(service_name='time',
                               service_type=SoPServiceType.VALUE, policy=SoPPolicy.ALL)

        return self.handle_result_list(result_list)

    def test_request_line(self) -> bool:
        result_list = self.r('(#Hue).on()')
        result_list = self.r('(#Hue).set_brightness($1)', 100)
        result_list = self.r('(#Hue).off()')

        return self.handle_result_list(result_list)


def arg_parse():
    parser = argparse.ArgumentParser()
    # parser.add_argument("--log", action='store_true', dest='log',
    #                     required=False, default=True, help="make log file")
    parser.add_argument("--name", '-n', action='store',
                        required=False, default='TestSuperClient', help="client name")
    parser.add_argument("--host", '-ip', action='store',
                        required=False, default='147.46.114.165', help="host name")
    parser.add_argument("--port", '-p', action='store',
                        required=False, default=1883, help="port")
    parser.add_argument("--refresh_cycle", '-rc', action='store',
                        required=False, default=5, help="refresh_cycle")
    arg_list, unknown = parser.parse_known_args()

    return arg_list


def main():
    arg_list = arg_parse()
    client = SoPLevel1SuperThing(name='SuperThingTest', ip='147.46.114.165', port=21283,
                                 refresh_cycle=10)
    # client = SoPLevel1SuperClient(name='TestSuperClient',
    #                               ip='147.46.216.33', port=10883, refresh_cycle=5)
    client.setup(avahi_enable=False)
    client.run()


if __name__ == '__main__':
    main()
