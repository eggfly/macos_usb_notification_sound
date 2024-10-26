#!/usr/bin/env python3
import sys
# 重定向标准输出
class NullWriter:
    def write(self, arg):
        pass

    def flush(self):
        pass

original_stdout = sys.stdout
sys.stdout = NullWriter()

import pygame
# pygame.init()

sys.stdout = original_stdout

import subprocess
import threading
import time
import difflib
from queue import Queue


connect_sound_file = 'usb_sound_windows_10_connect.mp3'
disconnect_sound_file = 'windows-10-usb-disconnect-sound-effect.mp3'

play_audio_queue = Queue()


def play_audio_files():
    # 初始化pygame混音器
    pygame.mixer.init()


    # 保持程序运行，直到音乐播放结束
    while True:
        audio_file = play_audio_queue.get()
        # 加载MP3文件
        pygame.mixer.music.load(audio_file)
        # 播放音乐
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

def query_usb_device_by_command():
    proc = subprocess.Popen(['system_profiler', 'SPUSBDataType'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    ret = proc.communicate()
    stdout = ret[0]
    return stdout

def calc_diff_info(prev, current):
    before_lines = prev.decode('utf-8').strip().splitlines()
    after_lines = current.decode('utf-8').strip().splitlines()
    diff = difflib.unified_diff(before_lines, after_lines, lineterm='', fromfile='before', tofile='after')

    added_lines = 0
    removed_lines = 0
    content = '\n'.join(diff)
    for line in diff:
        if line.startswith('+') and not line.startswith('+++'):
            added_lines += 1
        elif line.startswith('-') and not line.startswith('---'):
            removed_lines += 1
    return content, added_lines, removed_lines

def poll_usb_devices():
    prev_device_result = None
    while True:
        device_result = query_usb_device_by_command()
        changed = False
        if prev_device_result is not None and prev_device_result != device_result:
            diff_content, added, removed = calc_diff_info(prev_device_result, device_result)
            print(diff_content)
            if len(device_result) > len(prev_device_result):
                print('USB device connected!')
                play_audio_queue.put(connect_sound_file)
            else:
                print('USB device disconnected!')
                play_audio_queue.put(disconnect_sound_file)
            changed = True
        prev_device_result = device_result
        if not changed:
            time.sleep(0.5)


def main():
    poll_thread = threading.Thread(target=poll_usb_devices)
    play_thread = threading.Thread(target=play_audio_files)
    poll_thread.start()
    play_thread.start()


if __name__ == '__main__':
    main()
