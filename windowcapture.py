import numpy as np
from threading import Thread, Lock
import mss


class WindowCapture:

    # threading properties
    stopped = True
    lock = None
    screenshot = None
    # properties
    monitor = 1

    # constructor
    def __init__(self, monitor_num=None):
        # create a thread lock object
        self.lock = Lock()

        if monitor_num is None:
            # self.hwnd = win32gui.GetDesktopWindow()
            self.monitor = 1
        else:
            self.monitor = monitor_num

    def get_screenshot(self):
        with mss.mss() as mss_instance:
            monitor_instance = mss_instance.monitors[self.monitor]
            img = mss_instance.grab(monitor_instance)  # Take the screenshot
            img = np.array(img)  # convert to usable array
            return img

    # threading methods
    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def stop(self):
        self.stopped = True

    def run(self):
        while not self.stopped:
            # get an updated image of the game
            screenshot = self.get_screenshot()
            # lock the thread while updating the results
            self.lock.acquire()
            self.screenshot = screenshot
            self.lock.release()
