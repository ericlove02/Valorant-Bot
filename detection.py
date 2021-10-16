import cv2 as cv
from threading import Thread, Lock
from PIL import Image
from itertools import product
import numpy as np
from matplotlib import cm


class Detection:

    # threading properties
    stopped = True
    lock = None
    rectangles = set()
    # properties
    cascade = None
    screenshot = None

    # pixel search color properties
    r_min = 20
    r_max = 41
    g_min = 110
    g_max = 126
    b_min = 50
    b_max = 111

    def __init__(self, model_file_path):
        # create a thread lock object
        self.lock = Lock()
        # load the trained model
        self.cascade = cv.CascadeClassifier(model_file_path)

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
        while not self.stopped:
            if self.screenshot is not None:
                # do object detection
                # self.rectangles = self.cascade.detectMultiScale(self.screenshot)
                img = self.screenshot
                img = np.resize(img, (30, 30))
                img = Image.fromarray(np.uint8(cm.gist_earth(img) * 255))
                rgb = img.convert('RGB')
                for x in range(img.size[0]):
                    for y in range(img.size[1]):
                        r, g, b = rgb.getpixel((x, y))
                        print(str(r) + ", " + str(b) + ", " + str(g))
                        if self.r_min <= r <= self.r_max and self.b_min <= b <= self.b_max and self.g_min <= g <= self.g_max:
                            print("\nFOUND\n")
                            self.rectangles.add((x, y, 30, 30))

                # lock the thread while updating the results
                self.lock.acquire()
                self.rectangles = self.rectangles
                self.lock.release()
