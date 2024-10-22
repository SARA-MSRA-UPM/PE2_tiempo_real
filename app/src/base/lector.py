# external imports
from threading import Thread, Event
# internal imports
from .monitor import Monitor
from ..helpers.helpers import radar_detection_to_point


class Lector(Thread):
    def __init__(self, monitor: Monitor):
        super().__init__()

        self._monitor = monitor

        self._stop_event = Event()

    def run(self):
        while not self._stop_event.is_set():
            detection = self._monitor.take_first_detection()
            point = radar_detection_to_point(detection=detection)

    def stop(self):
        self._stop_event.set()
