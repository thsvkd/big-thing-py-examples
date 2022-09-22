#!/bin/python

from big_thing_py.big_thing import *

import argparse
import time
import board
import adafruit_tsl2591
import adafruit_bme280.advanced as adafruit_bme280
import adafruit_sgp30

i2c = board.I2C()

tsl2591 = adafruit_tsl2591.TSL2591(i2c)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)


def setup_tsl2591():
    # tsl2591.gain = adafruit_tsl2591.GAIN_LOW # (1x gain)
    tsl2591.gain = adafruit_tsl2591.GAIN_MED  # (25x gain, the default)
    # tsl2591.gain = adafruit_tsl2591.GAIN_HIGH # (428x gain)
    # tsl2591.gain = adafruit_tsl2591.GAIN_MAX # (9876x gain)
    # tsl2591.integration_time = adafruit_tsl2591.INTEGRATIONTIME_100MS # (100ms, default)
    # tsl2591.integration_time = adafruit_tsl2591.INTEGRATIONTIME_200MS # (200ms)
    # tsl2591.integration_time = adafruit_tsl2591.INTEGRATIONTIME_300MS # (300ms)
    # tsl2591.integration_time = adafruit_tsl2591.INTEGRATIONTIME_400MS # (400ms)
    # tsl2591.integration_time = adafruit_tsl2591.INTEGRATIONTIME_500MS # (500ms)
    # tsl2591.integration_time = adafruit_tsl2591.INTEGRATIONTIME_600MS # (600ms)


def setup_bme280():
    # Change this to match the location's pressure (hPa) at sea level
    bme280.sea_level_pressure = 1013.25
    bme280.mode = adafruit_bme280.MODE_NORMAL
    bme280.standby_period = adafruit_bme280.STANDBY_TC_500
    bme280.iir_filter = adafruit_bme280.IIR_FILTER_X16
    bme280.overscan_pressure = adafruit_bme280.OVERSCAN_X16
    bme280.overscan_humidity = adafruit_bme280.OVERSCAN_X1
    bme280.overscan_temperature = adafruit_bme280.OVERSCAN_X2
    # The sensor will need a moment to gather initial readings
    time.sleep(1)


def setup_sgp30():
    sgp30.iaq_init()
    sgp30.set_iaq_baseline(0x8973, 0x8aae)


def sensor_init():
    setup_tsl2591()
    setup_bme280()
    setup_sgp30()


def sense_temp():
    print("\nTemperature: %0.1f C" % bme280.temperature)
    return bme280.temperature


def sense_humid():
    print("Humidity: %0.1f %%" % bme280.relative_humidity)
    return bme280.relative_humidity


def sense_pressure():
    print("Pressure: %0.1f hPa" % bme280.pressure)
    print("Altitude = %0.2f meters" % bme280.altitude)
    return bme280.pressure


def sense_CO2():
    print("eCO2 = %d ppm" % (sgp30.eCO2))
    return sgp30.eCO2


def sense_brightness():
    lux = tsl2591.lux
    print("Total light: {0}lux".format(lux))
    # You can also read the raw infrared and visible light levels.
    # These are unsigned, the higher the number the more light of that type.
    # There are no units like lux.
    # Infrared levels range from 0-65535 (16-bit)
    infrared = tsl2591.infrared
    print("Infrared light: {0}".format(infrared))
    # Visible-only levels range from 0-2147483647 (32-bit)
    visible = tsl2591.visible
    print("Visible light: {0}".format(visible))
    # Full spectrum (visible + IR) also range from 0-2147483647 (32-bit)
    full_spectrum = tsl2591.full_spectrum
    print("Full spectrum (IR + visible) light: {0}".format(full_spectrum))

    return lux


def sense_sound():
    return 50


def sense_dust():
    return 50


def sense_VOC():
    print("TVOC = %d ppb" % (sgp30.TVOC))
    return sgp30.TVOC


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", action='store_true', dest='log',
                        required=False, default=True, help="enable log to file")
    parser.add_argument("--name", '-n', action='store',
                        required=False, default='sensor_box_thing', help="thing name")
    parser.add_argument("--host", '-h', action='store',
                        required=False, default='127.0.0.1', help="host name")
    parser.add_argument("--port", '-p', action='store',
                        required=False, default=1883, help="port")
    parser.add_argument("--refresh_cycle", '-rc', action='store',
                        required=False, default=5, help="refresh_cycle")
    parser.add_argument("--append_mac", '-am', action='store_true',
                        required=False, help="append mac address to thing's name")
    arg_list, unknown = parser.parse_known_args()

    return arg_list


def main():
    tags = [SoPTag(name='sensor_box'), ]

    value_temp = SoPValue(name='temp',
                          function=sense_temp,
                          type='double',
                          bound=(-100, 100),
                          tag_list=tags,
                          cycle=1)
    value_humid = SoPValue(name='humid',
                           function=sense_humid,
                           type='double',
                           bound=(0, 100),
                           tag_list=tags,
                           cycle=1)
    value_pressure = SoPValue(name='pressure',
                              function=sense_pressure,
                              type='double',
                              bound=(0, 10000),
                              tag_list=tags,
                              cycle=1)
    value_CO2 = SoPValue(name='CO2',
                         function=sense_CO2,
                         type='int',
                         bound=(0, 10000),
                         tag_list=tags,
                         cycle=1)
    value_brightness = SoPValue(name='brightness',
                                function=sense_brightness,
                                type='int',
                                bound=(0, 10000),
                                tag_list=tags,
                                cycle=1)
    value_sound = SoPValue(name='sound',
                           function=sense_sound,
                           type='int',
                           bound=(0, 10000),
                           tag_list=tags,
                           cycle=1)
    value_dust = SoPValue(name='dust',
                          function=sense_dust,
                          type='double',
                          bound=(0, 10000),
                          tag_list=tags,
                          cycle=1)
    value_VOC = SoPValue(name='VOC',
                         function=sense_VOC,
                         type='double',
                         bound=(0, 10000),
                         tag_list=tags,
                         cycle=1)

    thing = SoPThing(name='LocalClientDummy',
                     value_list=[value_temp,
                                 value_humid,
                                 value_pressure,
                                 value_CO2,
                                 value_brightness,
                                 value_sound,
                                 value_dust,
                                 value_VOC],
                     function_list=[],
                     alive_cycle=10)

    args = arg_parse()
    client = SoPBigThing(thing=args.name, ip=args.host, port=args.port)
    client.setup(avahi_enable=True)
    client.run()


if __name__ == '__main__':
    sensor_init()
    main()
