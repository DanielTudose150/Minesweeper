from time import sleep


class Countdown:
    def __init__(self, seconds):
        self.seconds = seconds
        self.finished = False

    def start(self):
        while self.seconds > 0:
            self.seconds -= 1
            sleep(1)
        self.finished = True

    def getSeconds(self):
        return self.seconds

    def getFinished(self):
        return self.finished
