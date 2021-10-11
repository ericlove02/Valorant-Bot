######################################################
# Valorant Aimbot project using opencv and pyautogui #
# Eric Love                                          #
######################################################

import cv2 as cv
import numpy as np
import pyautogui as pag
from time import time
import keyboard
from PIL import ImageGrab
import win32gui, win32ui, win32con


def window_capture:
    w = 1920  # set this
    h = 1080  # set this
    bmpfilenamename = "out.bmp"  # set this

    hwnd = win32gui.FindWindow(None, windowname)
    wDC = win32gui.GetWindowDC(hwnd)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0, 0), (w, h), dcObj, (0, 0), win32con.SRCCOPY)
    dataBitMap.SaveBitmapFile(cDC, bmpfilenamename)

    # Free Resources
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())


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
