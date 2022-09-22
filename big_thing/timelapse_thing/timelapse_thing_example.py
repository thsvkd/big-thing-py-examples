#!/bin/python

import time
import os
import os.path as op
import datetime
import argparse
from glob import glob
from tqdm import tqdm
import cv2

from big_thing_py.big_thing import *


# 현재 웹캠이 지원하는 해상도 출력
# v4l2-ctl -d /dev/video0 --list-formats-ext


# def input_char(message=''):
#     win = curses.initscr()
#     win.addstr(0, 0, message)

#     ch = win.getch()
#     if ch in range(32, 127):
#         curses.endwin()
#         time.sleep(0.05)
#         return chr(ch)
#     else:
#         time.sleep(0.05)
#         return None


def make_folder(folder):
    try:
        if not op.exists(folder):
            os.makedirs(folder)
    except OSError:
        print(
            f'[Error] Failed to create directory : {folder}')


def make_image_name(folder):
    now = datetime.datetime.now()
    now_datetime = now.strftime('%Y-%m-%d %H:%M:%S')
    capture_date = now.strftime('%Y%m%d')
    capture_time = now.strftime('%H%M%S')
    # capture_time = now.strftime('%H')

    image_name = '_'.join([capture_date, capture_time])
    image_name_duplicate = glob(
        f'{folder}/*{image_name}*.jpg')

    if len(image_name_duplicate) > 1:
        tmp_list = []
        for image in image_name_duplicate:
            name_split = image.split('_')
            if len(name_split) > 2:
                index = image.split('_')[-1][:-4]
                tmp_list.append(int(index))
        latest_index = max(tmp_list)

        image_name = '_'.join(
            [image_name, str(latest_index + 1)])
    elif len(image_name_duplicate) == 1:
        image_name += '_1'

    return image_name


class Timelapse():

    DEFAULT_IMAGE_FOLDER = 'capture_images'
    DEFAULT_VIDEO_FOLDER = 'video_out'
    DEFAULT_CONFIG_PATH = 'config.json'

    def __init__(self, width=1920, height=1080, fps=30.0, cap_num=1, cycle=1000):
        self.cap = None
        self.width = width
        self.height = height
        self.cap_num = cap_num
        self.fps = fps
        self.vout = None
        self.run_capture = False
        self.cycle = cycle
        self.capture_num = 0

        self.timelapse_event: Event = Event()
        self.timelapse_lock: Lock = Lock()
        self.timelapse_thread: Thread = Thread(
            target=self.run, daemon=True, args=(self.timelapse_event,))

    def set_width(self, width):
        self.width = width
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)

    def set_height(self, height):
        self.height = height
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

    def set_FPS(self, fps):
        self.fps = fps
        self.cap.set(cv2.CAP_PROP_FPS, self.fps)

    def make_video(self, src_path=DEFAULT_IMAGE_FOLDER, des_path=DEFAULT_VIDEO_FOLDER):
        print(f'Make video start. [video path : {des_path}]')
        image_list = glob(f'{src_path}/*.jpg')
        image_list.sort()
        size = (self.width, self.height)

        make_folder(des_path)

        self.vout = cv2.VideoWriter(
            f'{des_path}/out.mp4', cv2.VideoWriter_fourcc(*'H264'), self.fps, size)

        for image in tqdm(image_list, desc='image read'):
            frame = cv2.imread(image)
            self.vout.write(frame)
        self.vout.release()
        print(f'Make video finish. [video path : {des_path}]')

    def start_capture(self):
        if not self.run_capture:
            self.run_capture = True
        else:
            print('thread already run now')

    def stop_capture(self):
        if self.run_capture:
            self.run_capture = False
        else:
            print('thread already stop now')

    def cap_destroy(self):
        self.cap.release()

    # override of thread class
    def run(self, user_stop_event: Event, folder=DEFAULT_IMAGE_FOLDER):
        print(f'Capture start. [image path : ./{folder}/]')

        self.cap = cv2.VideoCapture(self.cap_num)
        if not self.cap.isOpened():
            for i in range(0, 10):
                self.cap = cv2.VideoCapture(i)
                if self.cap.isOpened():
                    print(f'Found /dev/video{i}')
                    break
            else:
                print('Web cam is not available!')

        self.set_width(self.width)
        self.set_height(self.height)

        prev_millis = 0
        try:
            while not user_stop_event.wait(timeout=0.1):
                if (int(round(time.time() * 1000)) - prev_millis) > self.cycle and self.run_capture:
                    prev_millis = int(round(time.time() * 1000))
                    ret, frame = self.cap.read()
                    if ret:
                        make_folder(folder)
                        image_name = make_image_name(folder)
                        now_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                        cv2.imwrite(f'{folder}/{image_name}.jpg', frame)
                        print(
                            f'[{now_datetime}] Capture success! [press "v" to make video]\r')
                        self.capture_num += 1
                    else:
                        print('Camera capture failed!')
        except KeyboardInterrupt:
            print('KeyboardInterrupt... end timelapse')
            return False
        except Exception as e:
            print('while loop end')

    def run_thread(self):
        self.timelapse_thread.start()


timelapse = Timelapse()


@static_vars(flag=False, start_time=0)
def sense_time_passed():
    if not sense_time_passed.flag:
        sense_time_passed.flag = True
        sense_time_passed.start_time = time.time()
    return time.time() - sense_time_passed.start_time


def sense_capture_picture_num():
    return timelapse.capture_num


def actuate_timelapse_start():
    timelapse.start_capture()


def actuate_timelapse_stop():
    timelapse.stop_capture()


def actuate_timelapse_makevideo():
    timelapse.make_video()


def arg_parse():
    parser = argparse.ArgumentParser()
    # parser.add_argument("--log", action='store_true', dest='log',
    #                     required=False, default=True, help="make log file")
    parser.add_argument("--name", '-n', action='store',
                        required=False, default='TestSuperClient', help="client name")
    parser.add_argument("--host", '-ip', action='store',
                        required=False, default='192.168.50.181', help="host name")
    parser.add_argument("--port", '-p', action='store',
                        required=False, default=1883, help="port")
    parser.add_argument("--refresh_cycle", '-rc', action='store',
                        required=False, default=5, help="refresh_cycle")
    args, unknown = parser.parse_known_args()

    return args


def main():
    timelapse.run_thread()
    timelapse_tag = SoPTag(name='timelapse')

    arg_cam = SoPArgument(name='arg_cam',
                          type='int',
                          bound=(0, 100))
    arg_cycle = SoPArgument(name='arg_cycle',
                            type='int',
                            bound=(0, 99999999))
    arg_w = SoPArgument(name='arg_w',
                        type='int',
                        bound=(0, 99999))
    arg_h = SoPArgument(name='arg_h',
                        type='int',
                        bound=(0, 99999))

    function_timelapse_start = SoPFunction(name='timelapse_start',
                                           func=actuate_timelapse_start,
                                           return_type='void',
                                           tag_list=[timelapse_tag, ],
                                           arg_list=[])
    function_timelapse_stop = SoPFunction(name='timelapse_stop',
                                          func=actuate_timelapse_stop,
                                          return_type='void',
                                          tag_list=[timelapse_tag, ],
                                          arg_list=[])
    function_timelapse_makevideo = SoPFunction(name='timelapse_makevideo',
                                               func=actuate_timelapse_makevideo,
                                               return_type='void',
                                               tag_list=[timelapse_tag, ],
                                               arg_list=[])
    value_time_passed = SoPValue(name='time_passed',
                                 function=sense_time_passed,
                                 type='int',
                                 bound=(0, 100),
                                 tag_list=[timelapse_tag, ],
                                 cycle=1)
    value_capture_picture_num = SoPValue(name='capture_picture_num',
                                         function=sense_capture_picture_num,
                                         type='int',
                                         bound=(0, 100),
                                         tag_list=[timelapse_tag, ],
                                         cycle=1)

    thing = SoPThing(name='Timelapse',
                     value_list=[value_time_passed,
                                 value_capture_picture_num],
                     function_list=[function_timelapse_start,
                                    function_timelapse_stop, function_timelapse_makevideo],
                     alive_cycle=10)

    args = arg_parse()
    client = SoPLocalClient(thing=thing, ip='147.46.216.33',
                            port=12883)
    client.setup(avahi_enable=True)
    client.run()


if __name__ == '__main__':
    main()
