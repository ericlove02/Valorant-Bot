# DEPRECATED, content used in main to increase FPS

import cv2 as cv
from threading import Thread, Lock
from PIL import Image
from itertools import product
import numpy as np
from matplotlib import cm
import torch
import torch.nn as nn
import torch.optim as optim
from time import sleep, time
import pandas as pd
from termcolor import colored


class Detection:

    # threading properties
    stopped = True
    lock = None
    rectangles = set()
    # properties
    cascade = None
    screenshot = None
    loop_time = time()

    # pixel search color properties
    r_min = 20
    r_max = 41
    g_min = 110
    g_max = 126
    b_min = 50
    b_max = 111

    model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt', force_reload=True)
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
    model.conf = 0.45  # base confidence threshold (or base detection (0-1)
    model.iou = 0.45  # NMS IoU (0-1)
    print("model config complete")

    def __init__(self, model_file_path):
        # create a thread lock object
        self.lock = Lock()
        # load the trained model
        # self.cascade = cv.CascadeClassifier(model_file_path)

    def update(self, screenshot):
        self.lock.acquire()
        self.screenshot = screenshot
        self.lock.release()

    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def stop(self):
        self.stopped = True

    def run(self):
        # TODO: you can write your own time/iterations calculation to determine how fast this is
        loop_time = time()
        while not self.stopped:
            if self.screenshot is not None:
                frame = self.screenshot
                results = self.model(frame)
                print('FPS {}\n'.format(1 / (time() - loop_time)))
                if len(results.xyxy[0]) != 0:
                    print(colored("PLAYER DETECTED, " + str(len(results.xyxy[0])), "green"))
                    for *box, conf, cls in results.xyxy[0]:
                        x1y1 = [int(x.item()) for x in box[:2]]
                        x2y2 = [int(x.item()) for x in box[2:]]
                        x1, y1, x2, y2, conf = *x1y1, *x2y2, conf.item()
                        width = x2 - x1
                        height = y2 - y1

                # lock the thread while updating the results
                self.lock.acquire()
                self.rectangles = self.rectangles
                self.lock.release()
