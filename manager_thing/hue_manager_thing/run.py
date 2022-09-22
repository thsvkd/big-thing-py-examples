from hue_manager_thing import *
from hue_staff_thing import *


def main():
    client = SoPHueManagerThing(ip='147.46.114.124', port=32883,
                                bridge_ip='http://147.46.114.165/api/', bridge_port=80,
                                user_key='L-idzo6XFfRVA-DzXyA66xKzi-KxIJA75neakYyS', mode=SoPManagerMode.SPLIT,
                                scan_cycle=10, conf_file_path='hue_room_conf.json')
    client.setup(avahi_enable=False)
    client.run()


if __name__ == '__main__':
    main()
