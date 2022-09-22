from rf_manager_thing import *

# rf_radio = RF24(22, 0)
if __name__ == "__main__":
    rf_manager_thing = SoPRFManagerThing(
        name='rf_manager_thing_test', port=32883, ip='147.46.114.124', network_type=SoPNetworkType.RF, mode=SoPManagerMode.JOIN,
        addresses=(0xFFFFFFFFFFF1, 0xFFFFFFFFFFF0), power_mode=SoPRFPowerMode.HIGH, alive_cycle=10)

    rf_manager_thing.setup(avahi_enable=False)
    rf_manager_thing.run()
