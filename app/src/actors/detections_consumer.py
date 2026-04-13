# external imports
from threading import Thread, Event
from time import sleep
# internal imports
from src.monitors.detections_monitor import DetectionsMonitor


class DetectionsConsumer(Thread):
    
    def __init__(
            self, 
            monitor: DetectionsMonitor
        ):
        super().__init__()
        self._stop_event = Event()
        self._monitor = monitor
        
    def run(self):
        while not self._stop_event.is_set():
            detections = self._monitor.get_data()
            # print(f"Consumer got detections: {len(detections)}")
            sleep(2)
            
    def stop(self):
        self._stop_event.set()
