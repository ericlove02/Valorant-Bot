######################################################
# Valorant Aimbot project using opencv and pyautogui #
# Eric Love                                          #
######################################################

from time import time, sleep

import cv2 as cv
import keyboard
import mouse
import numpy as np
import pyautogui as pag
import win32con
import win32gui
import win32ui
import imutils
from PIL import ImageGrab

from windowcapture import WindowCapture

TOGGLE_KEY = 'z'
EXIT_KEY = '`'


def get_screenshot():
    # define your monitor width and height
    w, h = 1920, 1080

    # for now we will set hwnd to None to capture the primary monitor
    # hwnd = win32gui.FindWindow(None, window_name)
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
    img = img[..., :3]

    # make image C_CONTIGUOUS to avoid errors with cv.rectangle()
    img = np.ascontiguousarray(img)

    return img


def mask_image(img):
    img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    lower_red = np.array([0, 50, 50])
    upper_red = np.array([10, 255, 255])
    mask0 = cv.inRange(img_hsv, lower_red, upper_red)

    lower_red = np.array([170, 50, 50])
    upper_red = np.array([180, 255, 255])
    mask1 = cv.inRange(img_hsv, lower_red, upper_red)

    mask = mask0 + mask1

    output_img = img.copy()
    output_img[np.where(mask == 0)] = 0

    output_hsv = img_hsv.copy()
    output_hsv[np.where(mask == 0)] = 0

    return output_hsv


def detect_players(img):
    hog = cv.HOGDescriptor()
    hog.setSVMDetector(cv.HOGDescriptor_getDefaultPeopleDetector())

    img = imutils.resize(img, width=min(500, img.shape[1]))

    (players, _) = hog.detectMultiScale(img,
                                        winStride=(5, 5),
                                        padding=(3, 3),
                                        scale=1.21)
    return players


def click_head(mouse_x, mouse_y):
    """use x,y coordinate of detected bots position and move the mouse and click"""
    mouse.move(mouse_x, mouse_y, duration=0.03)
    mouse.click(button="left")
    print("Mouse clicked\n")


fps_time = time()
botOn = True
while True:
    if botOn:
        # screenshot = get_screenshot()
        screenshot = cv.imread("test_image.jpg")
        screenshot = np.array(screenshot)
        masked_screenshot = mask_image(screenshot)

        detectedPlayers = detect_players(masked_screenshot)

        for (x, y, w, h) in detectedPlayers:
            cv.rectangle(masked_screenshot, (x, y),
                         (x + w, y + h),
                         (0, 0, 255), 2)

        cv.imshow('screenshot', masked_screenshot)

        print('FPS {}'.format(1 / (time() - fps_time)))
        fps_time = time()

        if keyboard.is_pressed(TOGGLE_KEY):
            botOn = False
            print("Bot toggled off\n")
            sleep(0.1)
    elif not botOn:
        botOn = False
        if keyboard.is_pressed(TOGGLE_KEY):
            botOn = True
            print("Bot toggled on\n")
            sleep(0.05)

    if cv.waitKey(1) == ord(EXIT_KEY):
        print("Exiting...")
        cv.destroyAllWindows()
        exit(0)


