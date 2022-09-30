from hejhome_manager_thing import *
from hejhome_staff_thing import *

import argparse


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", '-n', action='store', type=str,
                        required=False, default='hejhome_manager_thing', help="thing name")
    parser.add_argument("--host", '-ip', action='store', type=str,
                        required=False, default='127.0.0.1', help="host name")
    parser.add_argument("--port", '-p', action='store', type=int,
                        required=False, default=1883, help="port")
    parser.add_argument("--alive_cycle", '-ac', action='store', type=int,
                        required=False, default=60, help="alive cycle")
    parser.add_argument("--auto_scan", '-as', action='store_true',
                        required=False, help="middleware auto scan enable")
    parser.add_argument("--log", action='store_true', dest='log',
                        required=False, default=True, help="log enable")

    parser.add_argument("--bridge_host", '-bip', action='store', type=str,
                        required=False, default='https://goqual.io/openapi', help="bridge ip")
    parser.add_argument("--bridge_port", '-bp', action='store', type=int,
                        required=False, default=80, help="bridge port")
    parser.add_argument("--user_key", '-k', action='store', type=str,
                        required=False, default='16502431-6249-474c-aeb0-f2d18e66aaac', help="user_key")
    parser.add_argument("--scan_cycle", '-sc', action='store', type=int,
                        required=False, default=60, help="scan_cycle")
    parser.add_argument("--mode", '-md', action='store', type=str,
                        required=False, default=SoPManagerMode.SPLIT.value, help="scan_cycle")
    arg_list, unknown = parser.parse_known_args()

    return arg_list


def generate_thing(args):
    thing = SoPHejhomeManagerThing(name=args.name, ip=args.host, port=args.port,
                                   bridge_ip=args.bridge_host, bridge_port=args.bridge_host,
                                   user_key=args.user_key, mode=SoPManagerMode.get(
                                       args.mode),
                                   scan_cycle=args.scan_cycle,
                                   alive_cycle=args.alive_cycle,
                                   conf_file_path='hejhome_room_conf.json',
                                   append_mac_address=args.append_mac)
    return thing


if __name__ == '__main__':
    args = arg_parse()
    thing = generate_thing(args)
    thing.setup(avahi_enable=args.auto_scan)
    thing.run()
