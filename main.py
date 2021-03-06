import cv2 as cv
import numpy as np
import os
from windowcapture import WindowCapture
# from detection import Detection
from bot import ValBot, BotState
from termcolor import colored
import torch
from threading import Thread, Lock
from PIL import Image
from itertools import product
from matplotlib import cm
import torch
import torch.nn as nn
import torch.optim as optim
from time import sleep, time
import pandas as pd
from termcolor import colored
import mss
from datetime import datetime
from threading import Thread, Lock
from movement import Movement

DEBUG = True
IN_GAME = False

# initialize the WindowCapture class
wincap = WindowCapture(1)
# load the detector
# load an empty Vision class
# vision = Vision()
# initialize the bot
bot = ValBot()
if IN_GAME:
    movement = Movement()


def main():
    torch.hub._validate_not_a_forked_repo = lambda a, b, c: True
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt')  # , force_reload=True)
    print("model loaded")
    if torch.cuda.is_available():
        if "16" in torch.cuda.get_device_name(
                torch.cuda.current_device()):  # known error with the 1650 GPUs where detection doesn't work
            print(colored("[!] CUDA ACCELERATION IS UNAVAILABLE (ISSUE WITH 1650/1660 GPUs)", "red"))
            exit(1)
        else:
            print(colored("CUDA ACCELERATION [ENABLED]", "green"))
    else:
        print(colored("[!] CUDA ACCELERATION IS UNAVAILABLE", "red"))
        print(colored("[!] Check your PyTorch installation, else performance will be very poor", "red"))
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print("modeling to: " + device)
    model.to(device)
    model.conf = 0.6  # base confidence threshold (or base detection (0-1)
    model.iou = 0.45  # NMS IoU (0-1)
    print("model config complete")

    loop_time = time()
    while True:

        # if we don't have a screenshot yet, don't run the code below this point yet
        if wincap.screenshot is None:
            continue

        frame = wincap.screenshot
        results = model(frame)
        targets = []
        if len(results.xyxy[0]) != 0:
            print(colored("PLAYER DETECTED, " + str(len(results.xyxy[0])), "green"))
            for *box, conf, cls in results.xyxy[0]:
                x1y1 = [int(x.item()) for x in box[:2]]
                x2y2 = [int(x.item()) for x in box[2:]]
                x1, y1, x2, y2, conf = *x1y1, *x2y2, conf.item()
                width = x2 - x1
                height = y2 - y1
                head = [int(x1 + width/2), int(y1 + height/12)]
                head_and_height = [int(x1 + width/2), int(y1 + height/12), height]
                # player detected with head at {head}
                targets.append(head_and_height)
                if DEBUG:
                    # draw the detection results onto the original image
                    cv.rectangle(frame, x1y1, x2y2, (244, 113, 115), 2)
                    cv.circle(frame, head, int(height/12), (0, 0, 255), 1)
                    cv.putText(frame, f"{int(conf * 100)}%", x1y1, cv.FONT_HERSHEY_DUPLEX, 1, (244, 113, 116), 2)
            bot.update_targets(targets)

        bot.update_screenshot(wincap.screenshot)
        if DEBUG:
            # draw useful information onto image
            cv.putText(frame, "Players Detected: {0}".format(len(results.xyxy[0])), (5, 80), cv.FONT_HERSHEY_DUPLEX, 1.2, (0, 200, 0), 2)
            fps = 1 / (time() - loop_time)
            if fps <= 5:
                cv.putText(frame, "LOW FPS WARNING", (190, 45), cv.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2,
                           cv.LINE_AA)
                print(colored("LOW FPS WARNING", "red"))
            cv.putText(frame, "FPS: {0}".format(str(int(fps))), (5, 45), cv.FONT_HERSHEY_SIMPLEX, 1.5, (255, 100, 0), 2,
                       cv.LINE_AA)
            cv.putText(frame, str(datetime.now().strftime("%H:%M:%S")), (5, 1430), cv.FONT_HERSHEY_SIMPLEX, 1.5,
                       (255, 100, 0), 2,
                       cv.LINE_AA)
            # resize and display the image
            dim = (1080, 608)
            frame = cv.resize(frame, dim)
            cv.imshow('Matches', frame)

            loop_time = time()

        # press '`' with the output window focused to exit.
        # waits 1 ms every loop to process key presses
        key = cv.waitKey(1)
        if key == ord('`'):
            wincap.stop()
            bot.stop()
            if IN_GAME:
                movement.stop()
            cv.destroyAllWindows()
            print('Done.')
            exit(0)


main = Thread(target=main)

main.start()
print("Main detection started")
wincap.start()
print("Window capture started")
bot.start()
print("Bot main started")
if IN_GAME:
    movement.start()
    print("Bot movement started")
