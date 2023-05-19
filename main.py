#!/usr/bin/env python3
import subprocess
import threading
import time
from queue import Queue

from playsound import playsound

connect_sound_file = 'usb_sound_windows_10_connect.mp3'
disconnect_sound_file = 'windows-10-usb-disconnect-sound-effect.mp3'

play_audio_queue = Queue()


def play_audio_files():
    while True:
        audio_file = play_audio_queue.get()
        playsound(audio_file)


def query_usb_device_by_command():
    proc = subprocess.Popen(['system_profiler', 'SPUSBDataType'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    ret = proc.communicate()
    stdout = ret[0]
    return stdout


def poll_usb_devices():
    prev_device_result = None
    while True:
        device_result = query_usb_device_by_command()
        changed = False
        if prev_device_result is not None and prev_device_result != device_result:
            if len(device_result) > len(prev_device_result):
                print('usb device connected!')
                play_audio_queue.put(connect_sound_file)
            else:
                print('usb device disconnected!')
                play_audio_queue.put(disconnect_sound_file)
            changed = True
        prev_device_result = device_result
        if not changed:
            time.sleep(1)


def main():
    poll_thread = threading.Thread(target=poll_usb_devices)
    play_thread = threading.Thread(target=play_audio_files)
    poll_thread.start()
    play_thread.start()


if __name__ == '__main__':
    main()
