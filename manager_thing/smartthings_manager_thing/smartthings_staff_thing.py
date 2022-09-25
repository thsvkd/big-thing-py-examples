from smartthings_utils import *
from big_thing_py.big_thing import *


class SmartThingsStaffThing(SoPThing):
    def __init__(self, name=None, value_list: List[SoPValue] = [], function_list: List[SoPFunction] = [], alive_cycle=10, is_super=False, device_id=None):
        super().__init__(name=name, value_list=value_list,
                         function_list=function_list, alive_cycle=alive_cycle, is_super=is_super)
        self.device_id = device_id

    def get_device_id(self):
        return self.device_id

    def set_device_id(self, device_id):
        self.device_id = device_id
