#!/bin/python

from big_thing_py.big_thing import *

import argparse
import os

import picamera
from gtts import gTTS
from textblob import TextBlob

camera = picamera.PiCamera()


def speaker_speak(text: str) -> bool:
    lang = TextBlob(text).detect_language()
    SOPLOG_DEBUG(f'lang detected: {lang}')

    myobj = gTTS(text=text, lang=lang, slow=False)
    myobj.save("welcome.mp3")
    os.system("mpg321 welcome.mp3")

    return True


def camera_capture(file_name: str) -> bool:
    result = camera.capture(file_name)
    return True


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", '-n', action='store', type=str,
                        required=False, default='basic_thing', help="thing name")
    parser.add_argument("--host", '-ip', action='store', type=str,
                        required=False, default='127.0.0.1', help="host name")
    parser.add_argument("--port", '-p', action='store', type=int,
                        required=False, default=1883, help="port")
    parser.add_argument("--alive_cycle", '-ac', action='store', type=int,
                        required=False, default=60, help="alive cycle")
    parser.add_argument("--log", action='store_true', dest='log',
                        required=False, default=True, help="log enable")
    args, unknown = parser.parse_known_args()

    return args


def generate_thing(args):
    tag_list = [SoPTag(name='camera'),
                SoPTag(name='speaker')]
    function_list = [SoPFunction(func=speaker_speak,
                                 return_type='bool',
                                 tag_list=tag_list,
                                 arg_list=[SoPArgument(name='function_speak_arg',
                                                       type=SoPType.STRING,
                                                       bound=(0, 10000))]),
                     SoPFunction(func=camera_capture,
                                 return_type='bool',
                                 tag_list=tag_list,
                                 arg_list=[SoPArgument(name='function_camera_arg',
                                                       type=SoPType.STRING,
                                                       bound=(0, 10000))])]
    value_list = []

    thing = SoPBigThing(name=args.name, ip=args.host, port=args.port, alive_cycle=args.alive_cycle,
                        service_list=function_list + value_list)
    return thing


if __name__ == '__main__':
    camera.resolution = (2592, 1944)

    thing = generate_thing(arg_parse())
    thing.setup(avahi_enable=True)
    thing.run()
