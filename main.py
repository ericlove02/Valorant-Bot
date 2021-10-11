######################################################
# Valorant Aimbot project using opencv and pyautogui #
# Eric Love                                          #
######################################################

from time import time

import cv2 as cv
import numpy as np
import pyautogui as pag
import win32con
import win32gui
import win32ui

from windowcapture import WindowCapture

EXIT_KEY = '`'
TOGGLE_KEY = 'z'


def get_screenshot():
    # define your monitor width and height
    w, h = 1920, 1080

    # for now we will set hwnd to None to capture the primary monitor
    #hwnd = win32gui.FindWindow(None, window_name)
    hwnd = None

    # get the window image data
    wDC = win32gui.GetWindowDC(hwnd)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0, 0), (w, h), dcObj, (0, 0), win32con.SRCCOPY)

    # convert the raw data into a format opencv can read
    signedIntsArray = dataBitMap.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (h, w, 4)

    # free resources
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())

    # drop the alpha channel to work with cv.matchTemplate()
    img = img[...,:3]

    # make image C_CONTIGUOUS to avoid errors with cv.rectangle()
    img = np.ascontiguousarray(img)

    return img


def click_head(mouseX, mouseY):
    """use x,y coordinate of detected bots position and move the mouse and click"""
    # pag.move(mouseX, mouseY)
    pag.click()


# wincap = WindowCapture('(107) Fast Window Capture - OpenCV Object Detection in Games #4 - YouTube - Google Chrome')

fps_time = time()
while True:
    # get screenshots
    screenshot = get_screenshot()
    screenshot = np.array(screenshot)

    # masks
    img_hsv = cv.cvtColor(screenshot, cv.COLOR_BGR2HSV)

    lower_red = np.array([0, 50, 50])
    upper_red = np.array([10, 255, 255])
    mask0 = cv.inRange(img_hsv, lower_red, upper_red)

    lower_red = np.array([170, 50, 50])
    upper_red = np.array([180, 255, 255])
    mask1 = cv.inRange(img_hsv, lower_red, upper_red)

    mask = mask0 + mask1

    output_img = screenshot.copy()
    output_img[np.where(mask == 0)] = 0

    output_hsv = img_hsv.copy()
    output_hsv[np.where(mask == 0)] = 0

    cv.imshow('screenshot', output_hsv)

    print('FPS {}'.format(1 / (time() - fps_time)))
    fps_time = time()

    if cv.waitKey(1) == ord(EXIT_KEY):
        cv.destroyAllWindows()
        break

print("done")
