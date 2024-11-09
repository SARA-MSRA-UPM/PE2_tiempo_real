# external imports
from threading import Thread, Event
# internal imports
from .monitor import Monitor
from ..helpers.helpers import radar_detection_to_point
from ..graphics.map_view import MapView
from .detections_set import DetectionsSet


class Lector(Thread):
    def __init__(self, monitor: Monitor, view: MapView, detection_set: DetectionsSet):
        super().__init__()

        self._monitor = monitor
        self._view = view
        self._detection_set = detection_set

        self._stop_event = Event()

    def run(self):
        while not self._stop_event.is_set():
            detection = self._monitor.take_first_detection()
            point = radar_detection_to_point(detection=detection)
            self._detection_set.add_detection_to_the_set(detection)
            self._view.draw_detected_point(point, detection[0].name)

    def stop(self):
        self._stop_event.set()