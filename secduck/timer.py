import threading
import time


class Timer:
    def __init__(self):
        self.event = threading.Event()
        self.count = 0
        self.callback = lambda: None

    def run(self):
        while self.count > 0 and not self.event.is_set():
            self.count -= 1
            self.event.wait(1)

        if self.count <= 0:
            self.callback()

    def start(self, count, callback):
        self.event.clear()
        self.count = count
        self.callback = callback
        t = threading.Thread(target=self.run)
        t.start()

    def stop(self):
        self.event.set()
        self.count = 0

    def pause(self):
        self.event.set()

    def resume(self):
        self.event.clear()
        if self.count > 0:
            self.start(self.count, self.callback)

    def is_running(self):
        return not self.event.is_set()
