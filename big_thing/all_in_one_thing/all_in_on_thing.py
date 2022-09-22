#!/bin/python

from big_thing_py.big_thing import *

import argparse
import os

import picamera
from gtts import gTTS
from textblob import TextBlob

camera = picamera.PiCamera()


def actuate_speak(text):
    lang = TextBlob(text).detect_language()
    print(f'lang detected: {lang}')
    # url = 'https://kakaoi-newtone-openapi.kakao.com/v1/synthesize'
    # user_key = '5f04c8b832a65a0684176a447cdf7162'
    # header = {
    #     'Content-Type': 'application/xml',
    #     'Authorization': f'Authorization: KakaoAK {user_key}]',
    #     # 'Host': self.bridge_ip,
    #     # 'Referer': 'https://{host}'.format(host=self.host),
    #     # 'Accept': '*/*',
    #     # 'Connection': 'close',
    # }
    # body = f'<speak> {text} </speak>'
    # res = API_request(url=url, header=header, body=body,
    #                   method=RequestMethod.POST)

    myobj = gTTS(text=text, lang=lang, slow=False)
    myobj.save("welcome.mp3")
    os.system("mpg321 welcome.mp3")
    return True
    # if res:
    #     return True
    # else:
    #     return False


def actuate_capture():
    res = camera.capture('snapshot.jpg')
    return True


def actuate_show(color):
    return True


def arg_parse():
    parser = argparse.ArgumentParser()
    # parser.add_argument("--log", action='store_true', dest='log',
    #                     required=False, default=True, help="make log file")
    parser.add_argument("--name", '-n', action='store',
                        required=False, default='TestSuperClient', help="client name")
    parser.add_argument("--host", '-ip', action='store',
                        required=False, default='192.168.50.16', help="host name")
    parser.add_argument("--port", '-p', action='store',
                        required=False, default=1883, help="port")
    parser.add_argument("--refresh_cycle", '-rc', action='store',
                        required=False, default=5, help="refresh_cycle")
    arg_list, unknown = parser.parse_known_args()

    return arg_list


def main():
    tags = [SoPTag(name='all_in_one'), ]

    function_speak_arg = SoPArgument(
        name='function_speak_arg', type='string', bound=(0, 10000))
    function_speak_args = [function_speak_arg, ]
    function_speak = SoPFunction(name='speak',
                                 func=actuate_speak,
                                 return_type='bool',
                                 tag_list=tags,
                                 arg_list=function_speak_args)
    # function_capture_arg = SoPArgument(
    #     name='function_capture_arg', type='string', bound=(0, 10000))
    # function_capture_args = [function_capture_arg, ]
    function_capture = SoPFunction(name='capture',
                                   func=actuate_capture,
                                   return_type='bool',
                                   tag_list=tags,
                                   arg_list=[])
    function_show_arg = SoPArgument(
        name='function_show_arg', type='string', bound=(0, 10000))
    function_show_args = [function_show_arg, ]
    function_show = SoPFunction(name='show',
                                func=actuate_show,
                                return_type='bool',
                                tag_list=tags,
                                arg_list=function_show_args)

    thing = SoPThing(name='LocalClientDummy',
                     value_list=[],
                     function_list=[function_speak,
                                    function_capture,
                                    function_show],
                     alive_cycle=10)

    # client = SoPLocalClient(thing=thing, ip='192.168.50.181', port=1883)
    args = arg_parse()
    client = SoPLocalClient(thing=thing, ip=args.host, port=args.port)
    client.setup(avahi_enable=True)
    client.run()


if __name__ == '__main__':
    camera.resolution = (2592, 1944)
    sleep(2)
    main()
