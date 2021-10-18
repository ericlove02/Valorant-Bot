import cv2 as cv
import pyautogui
from time import sleep, time
from threading import Thread, Lock
from math import sqrt
# temp for testing
import mouse


class BotState:
    INITIALIZING = 0
    SEARCHING = 1
    MOVING = 2
    SHOOTING = 3
    BACKTRACKING = 4


class ValBot:
    # threading properties
    stopped = True
    lock = None

    # properties
    screenshot = None
    timestamp = None
    targets = []
    movement_screenshot = None
    window_offset = (0, 0)
    window_w = 0
    window_h = 0
    limestone_tooltip = None
    click_history = []

    def __init__(self):
        # create a thread lock object
        self.lock = Lock()

        # start bot in the initializing mode to allow us time to get setup.
        # mark the time at which this started so we know when to complete it
        self.state = BotState.INITIALIZING
        self.timestamp = time()

    def move_mouse(self, x, y, duration=.01):
        # moves mouse to desired location, returns true if success and false w error if unsuccessful
        # temporarily using mouse library for testing
        mouse.move(x, y, duration=duration)
        return True

    def click_mouse(self, button="left"):
        mouse.click(button=button)

    def click_target(self, coords):
        # get target from main detection to click on
        # might need to make more complex if targets are moving
        # need to pick best target if multiple given
        x, y = coords[0]
        coords.pop(0)
        self.move_mouse(x, y)
        # self.click_mouse()
        return coords

    def shoot_target(self, coords):
        # get target from main detection to click on
        # might need to make more complex if targets are moving
        # need to pick best target if multiple given
        x, y = coords[0]
        coords.pop(0)
        self.move_mouse(x, y)
        # self.click_mouse()
        return coords

    # threading methods
    def update_targets(self, targets):
        self.lock.acquire()
        self.targets = targets
        self.lock.release()

    def update_screenshot(self, screenshot):
        self.lock.acquire()
        self.screenshot = screenshot
        self.lock.release()

    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def stop(self):
        self.stopped = True

    # main logic controller
    def run(self):
        while not self.stopped:
            while True:
                sleep(.001)
                if self.targets:
                    self.targets = self.click_target(self.targets)

