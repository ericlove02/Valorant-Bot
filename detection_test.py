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
import mss

from windowcapture import WindowCapture

screenshot = None
loop_time = time()


wincap = WindowCapture(1)
wincap.start()
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

while True:

    if wincap.screenshot is None:
        continue
    frame = wincap.screenshot
    results = model(frame)

    if len(results.xyxy[0]) != 0:
        print(colored("PLAYER DETECTED, " + str(len(results.xyxy[0])), "green"))
        for *box, conf, cls in results.xyxy[0]:
            x1y1 = [int(x.item()) for x in box[:2]]
            x2y2 = [int(x.item()) for x in box[2:]]
            x1, y1, x2, y2, conf = *x1y1, *x2y2, conf.item()
            width = x2 - x1
            height = y2 - y1
            cv.rectangle(frame, x1y1, x2y2, (244, 113, 115), 2)
            cv.putText(frame, f"{int(conf * 100)}%", x1y1, cv.FONT_HERSHEY_DUPLEX, 0.5, (244, 113, 116), 2)
    print('FPS {}\n'.format(1/(time() - loop_time)))
    cv.imshow('Vision', frame)
    loop_time = time()
    key = cv.waitKey(1)
    if key == ord('`'):
        wincap.stop()
        cv.destroyAllWindows()
        break
