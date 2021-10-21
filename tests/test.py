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

wincap = WindowCapture(None)

body_classifier = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_fullbody.xml')


def red_mask_image(img):
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

    img = imutils.resize(img, width=min(1080, img.shape[1]))

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
        screenshot = wincap.get_screenshot()
        screenshot = np.array(screenshot)
        screenshot = cv.GaussianBlur(screenshot, (5, 5), 0)
        red_masked_screenshot = red_mask_image(screenshot)

        # for i in range(20):
        #     keyboard.press('w')
        #     sleep(0.1)
        # keyboard.release('w')

        # gray = cv.cvtColor(red_masked_screenshot, cv.COLOR_BGR2GRAY)
        detectedPlayers = body_classifier.detectMultiScale(red_masked_screenshot, 1.1, 0)

        # detectedPlayers = detect_players(red_masked_screenshot)

        for (x, y, w, h) in detectedPlayers:
            cv.rectangle(red_masked_screenshot, (x, y),
                         (x + w, y + h),
                         (0, 0, 255), 2)
            click_head(x, y)

        cv.imshow('screenshot', red_masked_screenshot)

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
