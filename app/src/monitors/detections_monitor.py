# external imports
from threading import Condition
# internal imports
from src.models.radar_detection import RadarDetection


class DetectionsMonitor:
     
    def __init__(self):
        self.lock = Condition()
        self.data: list[RadarDetection] = []

    def update(self, detection: RadarDetection):
        with self.lock:
            self.data.append(detection)
            self.lock.notify_all()
    
    def get_first(self) -> RadarDetection:
        with self.lock:
            while not self.data:
                self.lock.wait()
            data = self.data.pop(0)
            return data

    def get_data(self) -> list[RadarDetection]:
        with self.lock:
            while not self.data:
                self.lock.wait()
            data = self.data.copy()
            self.data.clear()
            return data
