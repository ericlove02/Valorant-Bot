import keyboard
from time import sleep, time
from threading import Thread, Lock


# move the player around the map and try to find some targets
# going to need more complex navigation in the future, specific to the practice map
# might need its own thread and class
class Movement:
    # threading properties
    stopped = True
    lock = None

    def __init__(self):
        self.lock = Lock()
        self.timestamp = time()

    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def stop(self):
        self.stopped = True

    # main logic controller
    def run(self):
        while not self.stopped:
            keyboard.press('w')
            sleep(.5)
            keyboard.press_and_release('space')
            sleep(.3)
            keyboard.release('w')
            sleep(1)
