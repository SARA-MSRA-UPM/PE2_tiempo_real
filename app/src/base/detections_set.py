from threading import Condition

from app.src.actors.radar import Radar

# Use a set of points to avoid duplicates
class DetectionsSet:
    def __init__(self):

        # This is the structure that needs to be protected
        # Set of detections, which are tuples of radar, distance, and facing
        self._detection_set:set[tuple[any, float, float]] = set()

        # Lock for controlling access
        self._lock_condition = Condition()

    def add_detection_to_the_set(self, detection: tuple[Radar, float, float]):
        with self._lock_condition:
            self._detection_set.add(detection)
            self._lock_condition.notify_all()

    # The CDS takes everything, and he implements the logic of selecting the point
    # That's the reason why it needs to take every detection
    def take_every_detection(self) -> set[tuple[any, float, float]]:
        with self._lock_condition:
            while not self._detection_set:
                self._lock_condition.wait()

            # Cannot return the list directly, because you need to clear it after taking the detections
            all_detections:set[tuple[any, float, float]] = self._detection_set.copy()
            self._detection_set.clear()
            return all_detections