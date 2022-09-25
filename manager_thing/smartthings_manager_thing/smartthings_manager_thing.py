from big_thing_py.manager_thing import *
from smartthings_staff_thing import *
from smartthings_utils import *


class SoPSmartThingsManagerThing(SoPManagerThing):

    def __init__(self, ip='127.0.0.1', port=1883, bridge_ip='', bridge_port=80, user_key='', refresh_cycle=10, network=..., ssl_enable=False, ssl_ca_path: str = f'{get_project_root()}/CA/'):
        super().__init__(ip=ip, port=port, bridge_ip=bridge_ip, bridge_port=bridge_port,
                         user_key=user_key, scan_cycle=refresh_cycle, ssl_enable=ssl_enable, ssl_ca_path=ssl_ca_path)
        self._thing_list: List[SmartThingsStaffThing] = [
        ]
        self._bridge_ip = bridge_ip
        self._bridge_port = bridge_port
        self._user_key = user_key
        self._header = {
            "Authorization": f"Bearer {self._user_key}",
            # "Host": self.bridge_ip,
            # "Referer": "https://{host}".format(host=self.host),
            "Accept": "*/*",
            "Connection": "close",
            "Content-Type": "application/json;charset-UTF-8"
        }

    def get_staff_list(self):
        print('get staff things list...')
        return API_request(
            url=self._bridge_ip + "devices", header=self._header, body='')

    # override
    def setup_staff(self, staff_list: dict):
        for staff in staff_list['items']:
            if not staff['manufacturerName'] == 'Samsung Electronics':
                continue
            thing = self.create_staff(staff)
            if not thing in self._thing_list:
                self.add(thing)

    def create_staff(self, staff_info: dict) -> SmartThingsStaffThing:

        switch_on_function = SoPFunction(
            name='switch_on', func=self.switch_on,
            return_type=type_converter(get_function_return_type(self.switch_on)), arg_list=[])
        switch_off_function = SoPFunction(
            name='switch_off', func=self.switch_off,
            return_type=type_converter(get_function_return_type(self.switch_off)), arg_list=[])
        brightness_set_function = SoPFunction(
            name='brightness_set', func=self.brightness_set,
            return_type=type_converter(get_function_return_type(self.brightness_set)), arg_list=[])

        staff_function_list: List[SoPFunction] = [switch_on_function, switch_off_function,
                                                  brightness_set_function, ]
        staff_value_list: List[SoPValue] = []

        name = staff_info['name']
        deviceId: str = staff_info['deviceId']
        label = staff_info['label']

        for staff_function in staff_function_list:
            staff_function.add_tag(SoPTag('samsung'))
            staff_function.add_tag(SoPTag(label))
            staff_function.add_tag(SoPTag(name))
            staff_function.add_tag(SoPTag(deviceId.replace('-', '_')))

        for staff_value in staff_value_list:
            staff_value.add_tag(SoPTag('samsung'))
            staff_value.add_tag(SoPTag(label))
            staff_value.add_tag(SoPTag(name))
            staff_value.add_tag(SoPTag(deviceId.replace('-', '_')))

        staff_thing = SmartThingsStaffThing(
            name=label + '_' + deviceId.replace('-', '_'), value_list=staff_value_list, function_list=staff_function_list, alive_cycle=10, device_id=deviceId)
        return staff_thing

    # override
    def handle_function_actuate(self, stop_event: Event, lock: Lock):
        try:
            while not stop_event.wait(THREAD_TIME_OUT):
                if self._function_execute_queue.empty():
                    continue
                topic, payload = decode_MQTT_message(
                    self._function_execute_queue.get())

                target_function = topic.split('/')[1]
                target_thing = topic.split('/')[2]

                for thing in self._thing_list:
                    if not thing.get_registered() or thing.get_name() != target_thing:
                        continue
                    for function in thing.get_function_list():
                        function_name = function.get_name()
                        if function_name == target_function:
                            if function.get_enable_parallel():
                                self._device_id = thing.get_device_id()
                                function.execute(payload)
                            elif not function.get_processing():
                                self._device_id = thing.get_device_id()
                                function.execute(payload)
                            else:
                                SOPLOG_DEBUG(colored(
                                    f'function {function_name} is busy', 'yellow'))
                                self._function_execute_queue.put(
                                    encode_MQTT_message(topic, dict_to_json_string(payload)))
                            break
                    else:
                        SOPLOG_DEBUG(colored('function not exist', 'red'))
        except Exception as e:
            stop_event.set()
            SOPLOG_DEBUG(e, 'red')
            return False

    def setup(self, avahi_enable=True):
        return super().setup(avahi_enable=avahi_enable)

    def run(self, user_stop_event: Event = None, timeout=-1):
        return super().run(user_stop_event=user_stop_event, timeout=timeout)

    def wrapup(self):
        return super().wrapup()

    # staff values
    # def something(self):
    #     pass

    # staff functions
    def switch_on(self) -> bool:
        SOPLOG_DEBUG('switch_on actuate!!!', 'green')
        body = {
            'commands': [
                {
                    'component': 'main',
                    'capability': 'switch',
                    'command': 'on',
                    'arguments': []
                }
            ]
        }

        res = API_request(
            method=RequestMethod.POST,
            url=self._bridge_ip + 'devices/' + self._device_id + '/commands',
            body=dict_to_json_string(body),
            header=self._header,
            login_retry=False)

        if res:
            return True
        else:
            SOPLOG_DEBUG(
                f'[FUNC ERROR] API_request!!!', 'red')
            return False

    def switch_off(self) -> bool:
        SOPLOG_DEBUG('switch_off actuate!!!', 'green')
        body = {
            'commands': [
                {
                    'component': 'main',
                    'capability': 'switch',
                    'command': 'off',
                    'arguments': []
                }
            ]
        }

        res = API_request(
            method=RequestMethod.POST,
            url=self._bridge_ip + 'devices/' + self._device_id + '/commands',
            body=dict_to_json_string(body),
            header=self._header,
            login_retry=False)

        if res:
            return True
        else:
            SOPLOG_DEBUG(
                f'[FUNC ERROR] API_request!!!', 'red')
            return False

    def brightness_set(self, brightness: int) -> bool:
        SOPLOG_DEBUG('light_on actuate!!!', 'green')
        body = {
            'commands': [
                {
                    'component': 'main',
                    'capability': 'switchLevel',
                    'command': 'setLevel',
                    'arguments': [brightness]
                }
            ]
        }

        res = API_request(
            method=RequestMethod.POST,
            url=self._bridge_ip + 'devices/' + self._device_id + '/commands',
            body=dict_to_json_string(body),
            header=self._header,
            login_retry=False)

        if res:
            return True
        else:
            SOPLOG_DEBUG(
                f'[FUNC ERROR] API_request!!!', 'red')
            return False
