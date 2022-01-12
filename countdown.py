import time


class Countdown:
    def __init__(self, seconds):
        self.seconds = seconds

    def start(self):
        while self.seconds > 0:
            self.seconds -= 1
            time.sleep(1)

    def getSeconds(self):
        return self.seconds

    def getFinished(self):
        return self.finished
