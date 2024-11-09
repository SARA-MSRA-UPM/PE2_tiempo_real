from threading import Thread, Event
from time import sleep

from app.src.base.detections_set import DetectionsSet
from app.src.graphics.map_view import MapView
from app.src.helpers.helpers import radar_detection_to_point


class CommonDetectionsSearcher(Thread):
    def __init__(self, detection_set: DetectionsSet, view: MapView):
        super().__init__()

        # Distance threshold to consider two detections equal
        self._threshold = 5

        # The structure "consumed", protected by a monitor
        self._detections_set = detection_set

        self._view = view

        # Stop event
        self._stop_event = Event()

    def run(self):

        while not self._stop_event.is_set():
            # Search every 5 seconds, as stated in the requirements
            sleep(5)

            # Run the search
            self.search_common()

    def search_common(self):

        all_detections:set[tuple[any, float, float]] = self._detections_set.take_every_detection()

        already_considered:set[tuple[any, float, float]] = set()

        # Calculate distance between detections, and check it against the threshold
        for detection_origin in all_detections:

            # Transform the detection in a point
            point_origin = radar_detection_to_point(detection=detection_origin)

            # Compare against the other detections
            for detection_rest in all_detections:

                if detection_rest in already_considered:
                    continue

                # Transform the detection in a point
                point_rest = radar_detection_to_point(detection=detection_rest)

                # Difference vector
                difference_tuple = (point_rest.x - point_origin.x, point_rest.y - point_origin.y)

                # Difference magnitude
                difference_mod = (difference_tuple[0]**2 + difference_tuple[1]**2)**0.5

                # Check the threshold
                if (difference_mod < self._threshold) and (detection_origin[0] != detection_rest[0]):
                    print(f"Equal detections: Radar 1: {detection_origin[0].name} Radar 2: {detection_rest[0].name} x1: {point_origin.x} x2: {point_rest.x}  y1: {point_origin.y} y2: {point_rest.y}")
                    self._view.draw_detected_point(point_origin, "cds")
                    self._view.draw_detected_point(point_rest, "cds")

            already_considered.add(detection_origin)

    def stop(self):
        self._stop_event.set()