
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

# 初始化pygame混音器
pygame.mixer.init()


# 加载MP3文件
pygame.mixer.music.load('usb_sound_windows_10_connect.mp3')

# 播放音乐
pygame.mixer.music.play()

# 保持程序运行，直到音乐播放结束
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)
