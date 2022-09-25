
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
        try:
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

            return True
        except Exception as e:
            print_error(e)
            return False

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
