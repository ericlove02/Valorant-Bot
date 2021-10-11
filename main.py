######################################################
# Valorant Aimbot project using opencv and pyautogui #
# Eric Love                                          #
######################################################

import cv2 as cv
import keyboard
import numpy as np
import pyautogui as pag
from PIL import ImageGrab
from time import time
from windowcapture import WindowCapture

wincap = WindowCapture('Window Client')


def click_head(mouseX, mouseY):
    """use x,y coordinate of detected bots position and move the mouse and click"""
    print("click")


fps_time = time()
while True:

    screenshot = ImageGrab.grab()
    screenshot = np.array(screenshot)
    screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR)

    cv.imshow('screenshot', screenshot)

    print('FPS {}'.format(1 / (time() - fps_time)))
    fps_time = time()

    if cv.waitKey(1) == ord('`'):
        cv.destroyAllWindows()
        break

print("done")
