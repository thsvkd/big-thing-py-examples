from big_thing_py.manager_thing import *
from hue_utils import *


class SoPHueStaffThing(SoPStaffThing):
    def __init__(self, name=None, service_list: List[SoPService] = [], alive_cycle=10,  is_super=False, idx=None, bridge_ip=None, user_key=None, header=None, device_id=None):
        super().__init__(name=name, service_list=service_list,
                         alive_cycle=alive_cycle, device_id=device_id, is_super=is_super)
        self._idx = idx
        self._bridge_ip = bridge_ip.strip('/')
        self._user_key = user_key
        self._header = header

    def on(self) -> bool:
        SOPLOG_DEBUG('on actuate!!!', 'green')
        res: requests.Response = API_request(
            method=RequestMethod.PUT,
            url=f'{self._bridge_ip}/{self._user_key}/lights/{self._idx}/state',
            body=dict_to_json_string({'on': True}),
            header=self._header,
            login_retry=False)
        data = res.json()
        if 'success' in data[0]:
            return True
        else:
            return False

    def off(self) -> bool:
        SOPLOG_DEBUG(colored('off actuate!!!', 'green'))
        res: requests.Response = API_request(
            method=RequestMethod.PUT,
            url=f'{self._bridge_ip}/{self._user_key}/lights/{self._idx}/state',
            body=dict_to_json_string({'on': False}),
            header=self._header,
            login_retry=False)
        data = res.json()
        if 'success' in data[0]:
            return True
        else:
            return False

    def set_brightness(self, brightness: int) -> bool:
        SOPLOG_DEBUG('set_brightness actuate!!!', 'green')
        res: requests.Response = API_request(
            method=RequestMethod.PUT,
            url=f'{self._bridge_ip}/{self._user_key}/lights/{self._idx}/state',
            body=dict_to_json_string({'bri': int(brightness)}),
            header=self._header,
            login_retry=False)
        data = res.json()
        if 'success' in data[0]:
            return True
        else:
            return False

    def set_color(self, r, g, b) -> bool:
        SOPLOG_DEBUG('set_color actuate!!!', 'green')
        x, y = rgb_to_xy(float(r), float(g), float(b))
        res: requests.Response = API_request(
            method=RequestMethod.PUT,
            url=f'{self._bridge_ip}/{self._user_key}/lights/{self._idx}/state',
            body=dict_to_json_string({'xy': [x, y]}),
            header=self._header,
            login_retry=False)
        data = res.json()
        if 'success' in data[0]:
            return True
        else:
            return False

    def get_idx(self):
        return self._idx

    def set_idx(self, idx):
        self._idx = idx


class SoPHueGoStaffThing(SoPHueStaffThing):
    pass


class SoPHueStripStaffThing(SoPHueStaffThing):
    pass
