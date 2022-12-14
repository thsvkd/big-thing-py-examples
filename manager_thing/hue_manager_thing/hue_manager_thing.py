from big_thing_py.manager_thing import *
from hue_staff_thing import *
from hue_utils import *


class SoPHueManagerThing(SoPManagerThing):

    def __init__(self, name: str, service_list: List[SoPService], alive_cycle: float, is_super: bool = False, is_parallel: bool = True,
                 ip: str = None, port: int = None, ssl_ca_path: str = None, ssl_enable: bool = None, log_name: str = None, log_enable: bool = True, log_mode: SoPPrintMode = SoPPrintMode.ABBR, append_mac_address: bool = True,
                 mode: SoPManagerMode = SoPManagerMode.SPLIT, network_type: SoPNetworkType = SoPNetworkType.MQTT, scan_cycle=5,
                 bridge_ip: str = '', bridge_port: int = 80, user_key='', conf_file_path: str = 'hue_room_conf.json'):
        super().__init__(name, service_list, alive_cycle, is_super, is_parallel,
                         ip, port, ssl_ca_path, ssl_enable, log_name, log_enable, log_mode, append_mac_address,
                         mode, network_type, scan_cycle)
        self._child_thing_list: List[SoPHueStaffThing] = []
        self._conf_file_path = conf_file_path

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

    def setup(self, avahi_enable=True):
        self.load_config()

        return super().setup(avahi_enable=avahi_enable)

    # ===========================================================================================
    #  _    _                             _    __                      _    _
    # | |  | |                           | |  / _|                    | |  (_)
    # | |_ | |__   _ __   ___   __ _   __| | | |_  _   _  _ __    ___ | |_  _   ___   _ __   ___
    # | __|| '_ \ | '__| / _ \ / _` | / _` | |  _|| | | || '_ \  / __|| __|| | / _ \ | '_ \ / __|
    # | |_ | | | || |   |  __/| (_| || (_| | | |  | |_| || | | || (__ | |_ | || (_) || | | |\__ \
    #  \__||_| |_||_|    \___| \__,_| \__,_| |_|   \__,_||_| |_| \___| \__||_| \___/ |_| |_||___/
    # ===========================================================================================

    # nothing to add...

    # ====================================================================================================================
    #  _                        _  _        ___  ___ _____  _____  _____
    # | |                      | || |       |  \/  ||  _  ||_   _||_   _|
    # | |__    __ _  _ __    __| || |  ___  | .  . || | | |  | |    | |    _ __ ___    ___  ___  ___   __ _   __ _   ___
    # | '_ \  / _` || '_ \  / _` || | / _ \ | |\/| || | | |  | |    | |   | '_ ` _ \  / _ \/ __|/ __| / _` | / _` | / _ \
    # | | | || (_| || | | || (_| || ||  __/ | |  | |\ \/' /  | |    | |   | | | | | ||  __/\__ \\__ \| (_| || (_| ||  __/
    # |_| |_| \__,_||_| |_| \__,_||_| \___| \_|  |_/ \_/\_\  \_/    \_/   |_| |_| |_| \___||___/|___/ \__,_| \__, | \___|
    #                                                                                                         __/ |
    #                                                                                                        |___/
    # ====================================================================================================================

    # nothing to add...

    # ==================================================================================================================================
    #  _   _                    _  _                     _                   _                           _
    # | | | |                  | || |                   | |                 | |                         | |
    # | |_| |  __ _  _ __    __| || |  ___   ___  _   _ | |__   _ __    ___ | |_ __      __  ___   _ __ | | __  _ __ ___   ___   __ _
    # |  _  | / _` || '_ \  / _` || | / _ \ / __|| | | || '_ \ | '_ \  / _ \| __|\ \ /\ / / / _ \ | '__|| |/ / | '_ ` _ \ / __| / _` |
    # | | | || (_| || | | || (_| || ||  __/ \__ \| |_| || |_) || | | ||  __/| |_  \ V  V / | (_) || |   |   <  | | | | | |\__ \| (_| |
    # \_| |_/ \__,_||_| |_| \__,_||_| \___| |___/ \__,_||_.__/ |_| |_| \___| \__|  \_/\_/   \___/ |_|   |_|\_\ |_| |_| |_||___/ \__, |
    #                                                                                                                            __/ |
    #                                                                                                                           |___/
    # ==================================================================================================================================

    def _handle_staff_message(self, msg: str):
        protocol_type = None
        hue_device_list: Dict = msg

        for idx, hue_device in hue_device_list.items():
            if 'state' in hue_device:
                protocol_type = [
                    SoPProtocolType.Base.TM_REGISTER, SoPProtocolType.Base.TM_ALIVE]
                break

        if SoPProtocolType.Base.TM_REGISTER in protocol_type:
            self._handle_staff_REGISTER(msg)
        elif SoPProtocolType.Base.TM_ALIVE in protocol_type:
            self._handle_staff_ALIVE(msg)
        elif SoPProtocolType.Base.TM_VALUE_PUBLISH in protocol_type or SoPProtocolType.Base.TM_VALUE_PUBLISH_OLD in protocol_type:
            self._handle_staff_VALUE_PUBLISH(msg)
        elif SoPProtocolType.Base.TM_RESULT_EXECUTE in protocol_type:
            self._handle_staff_RESULT_EXECUTE(msg)

    # TODO: implement this
    def _send_staff_message(self, msg: Union[StaffRegisterResult, None]):
        if type(msg) == StaffRegisterResult:
            self._send_staff_RESULT_REGISTER(msg)
        elif type(msg) == None:
            pass
        else:
            self._publish_staff_packet(msg)

    def _handle_staff_REGISTER(self, msg):
        hue_device_list = msg

        for idx, staff_info in hue_device_list.items():
            staff_thing_info = SoPHueStaffThingInfo(device_id=staff_info['uniqueid'],
                                                    idx=idx, hue_info=staff_info)

            self._staff_register_queue.put(staff_thing_info)

    def _handle_staff_ALIVE(self, msg):
        hue_device_list = msg
        pass

    def _handle_staff_VALUE_PUBLISH(self, msg):
        hue_device_list = msg
        pass

    def _handle_staff_RESULT_EXECUTE(self, msg):
        hue_device_list = msg
        pass

    def _send_staff_RESULT_REGISTER(self, register_result: StaffRegisterResult):
        if register_result.device_id is None:
            raise ValueError('staff thing device_id is None')

        SOPLOG_DEBUG(
            f'[_send_staff_RESULT_REGISTER] Register {register_result.staff_thing_name} complete!!!')

    def _send_staff_EXECUTE(self, msg):
        pass

    # ========================
    #         _    _  _
    #        | |  (_)| |
    #  _   _ | |_  _ | | ___
    # | | | || __|| || |/ __|
    # | |_| || |_ | || |\__ \
    #  \__,_| \__||_||_||___/
    # ========================

    def _receive_staff_packet(self):
        cur_time = time.time()

        # for discover hue staff thing
        if cur_time - self._last_scan_time > self._scan_cycle:
            print('get staff things list...')

            hue_device_list = API_request(
                url=f'{self._bridge_ip}/{self._user_key}/lights', header=self._header, body='')
            for staff_thing in self._staff_thing_list:
                self._send_TM_ALIVE(staff_thing.get_name())
                staff_thing.set_last_alive_time(cur_time)
            if self.verify_hue_request_result(hue_device_list):
                self._last_scan_time = cur_time
                return hue_device_list
            else:
                return False
        else:
            for staff_thing in self._staff_thing_list:
                # for check hue staff thing alive
                if staff_thing.get_registered() and cur_time - staff_thing.get_last_alive_time() > staff_thing.get_alive_cycle():
                    hue_device_list = API_request(
                        url=f'{self._bridge_ip}/{self._user_key}/lights', header=self._header, body='')
                    if self.verify_hue_request_result(hue_device_list):
                        self._send_TM_ALIVE(staff_thing.get_name())
                        staff_thing.set_last_alive_time(cur_time)
                        return hue_device_list
                    else:
                        return False
                # for check hue staff thing value publish cycle
                else:
                    for value in staff_thing.get_value_list():
                        if cur_time - value.get_last_update_time() > value.get_cycle():
                            # update() method update _last_update_time of SoPValue
                            value.update()
                            self._send_TM_VALUE_PUBLISH(
                                value.get_name(), value.dump_pub())

        return None

    def _publish_staff_packet(self, msg):
        pass

    def load_config(self):
        conf_file = json_file_read(self._conf_file_path)

        # TODO: Thig code have some issue when conf file was not exist.... Fix it
        if conf_file:
            room_select = conf_file['select']
            hue_room_info = conf_file['room_list']
            for room in hue_room_info:
                if room_select == room['room_name']:
                    self._bridge_ip = room['bridge_ip'].strip('/')
                    self._bridge_port = int(room['bridge_port'])
                    self._user_key = room['user_key']
        elif self._bridge_ip == '' or self._bridge_ip == None:
            SOPLOG_DEBUG('bridge ip is empty. exit program...', 'red')
            raise Exception('HueConfigFileNotExist')

    def verify_hue_request_result(self, result_list: list):
        if type(result_list) == list and 'error' in result_list[0]:
            print_error(result_list[0]['error']['description'])
            return False
        else:
            return True

    def _create_staff(self, staff_thing_info: SoPHueStaffThingInfo) -> SoPHueStaffThing:
        staff_info = staff_thing_info.hue_info

        idx = staff_thing_info.idx
        name = staff_info['name'].replace(
            ' ', '_').replace('(', '_').replace(')', '_')
        uniqueid = staff_info['uniqueid']

        hue_child_thing = SoPHueStaffThing(
            name=name, service_list=[], alive_cycle=10, idx=idx, bridge_ip=self._bridge_ip, user_key=self._user_key, header=self._header, device_id=uniqueid)

        on_function = SoPFunction(
            name='on', func=hue_child_thing.on,
            return_type=type_converter(get_function_return_type(hue_child_thing.on)), arg_list=[], exec_time=10000, timeout=10000)

        off_function = SoPFunction(
            name='off', func=hue_child_thing.off,
            return_type=type_converter(get_function_return_type(hue_child_thing.off)), arg_list=[], exec_time=10000, timeout=10000)

        arg_brightness = SoPArgument(
            name='brightness', type=SoPType.INTEGER, bound=(0, 255))
        set_brightness_function = SoPFunction(
            name='set_brightness', func=hue_child_thing.set_brightness,
            return_type=type_converter(
                get_function_return_type(hue_child_thing.set_brightness)),
            arg_list=[arg_brightness], exec_time=10000, timeout=10000)

        arg_r = SoPArgument(
            name='r', type=SoPType.INTEGER, bound=(0, 255))
        arg_g = SoPArgument(
            name='g', type=SoPType.INTEGER, bound=(0, 255))
        arg_b = SoPArgument(
            name='b', type=SoPType.INTEGER, bound=(0, 255))
        set_color_function = SoPFunction(
            name='set_color', func=hue_child_thing.set_color,
            return_type=type_converter(
                get_function_return_type(hue_child_thing.set_color)),
            arg_list=[arg_r, arg_g, arg_b])

        staff_function_list: List[SoPService] = [on_function, off_function,
                                                 set_brightness_function, set_color_function]
        staff_value_list: List[SoPService] = []

        service_list: List[SoPService] = staff_function_list + staff_value_list

        for staff_service in service_list:
            staff_service.add_tag(SoPTag(name))
            staff_service.add_tag(SoPTag(uniqueid))
            staff_service.add_tag(SoPTag('Hue'))
            if 'lamp' in name.lower():
                staff_service.add_tag(SoPTag('professor'))
            hue_child_thing._add_service(staff_service)

        return hue_child_thing
