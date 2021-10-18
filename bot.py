import cv2 as cv
import pyautogui
from time import sleep, time
from threading import Thread, Lock
from math import sqrt
# temp for testing
import mouse
import keyboard


class BotState:
    INITIALIZING = 0
    SHOOTING = 1
    MOVING = 2
    RELOADING = 3


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
    end_time = None
    ammo = 25  # assuming Vandal is bought for each practice round

    def __init__(self):
        # create a thread lock object
        self.lock = Lock()

        # start bot in the initializing mode to allow us time to get setup.
        # mark the time at which this started so we know when to complete it
        self.state = BotState.INITIALIZING
        self.timestamp = time()
        sleep(5)

    def move_mouse(self):
        return True

    def move_mouseto(self, x, y, duration=.01):
        # moves mouse to desired location, returns true if success and false w error if unsuccessful
        # temporarily using mouse library for testing
        mouse.move(x, y, duration=duration)
        return True

    def click_mouse(self, button="left"):
        # mouse.click(button=button)
        pass

    def shoot_target(self, targets):
        # get target from main detection to click on
        # might need to make more complex if targets are moving
        # need to pick best target if multiple given
        target = self.get_best_targets(targets)
        x, y, height = target
        targets = []  # clear coords
        self.move_mouseto(x, y)
        keyboard.press("left ctrl")
        self.click_mouse()
        sleep(.1)
        keyboard.release("left ctrl")
        self.ammo -= 1
        print("Shot fired at: " + str(x) + ", " + str(y) + ". Ammo: " + str(self.ammo))
        return targets

    def get_best_targets(self, targets):
        # return the tallest target, closer targets will be taller
        # x, y, height = targets[0]
        best_target = None
        for (x, y, height) in targets:
            if best_target is None:
                best_target = [x, y, height]
            elif height >= best_target[2]:
                best_target = [x, y, height]
        print("Found best target with height " + str(best_target[2]))
        return best_target

    def reload(self):
        keyboard.press_and_release('r')
        print("reloaded")
        return 25

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
                    self.state = BotState.SHOOTING
                    self.targets = self.shoot_target(self.targets)
                elif self.ammo <= 8:  # if there are no targets in site and ammo is low
                    self.state = BotState.RELOADING
                    self.ammo = self.reload()
                else:
                    # if nothing in view, pan around for something
                    #self.move_mouse()
                    pass
