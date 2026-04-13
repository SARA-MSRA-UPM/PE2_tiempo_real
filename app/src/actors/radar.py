# external imports
import math
from threading import Thread, Event
from time import sleep
# internal imports
from src.actors.points.point import Point
from src.monitors.detections_monitor import DetectionsMonitor
from src.models.radar_detection import RadarDetection
from src.helpers.helpers import (
    translate_figure,
    rotate_figure
)

# Radar constants
TRIANGLE = [(0, 0.5), (0, -0.5), (1, 0)]
INCREMENT = 15
REVOLUTIONS = 1


class Radar(Thread):
    def __init__(
            self,
            name: str,
            position: tuple[float, float],
            detection_range: float,
            initial_orientation: float,
            increment: float,
            revolutions_per_second: int,
            detectable_points: list[Point],
            monitor: DetectionsMonitor,
        ):
        super().__init__()
        # Radar atributes
        self.name = name
        self.x, self.y = position
        self.detection_range = detection_range
        self.initial_orientation = initial_orientation
        self.facing = 0
        self.revolutions_per_second = revolutions_per_second
        self.increment = increment
        self.detections = set()
        self.detectable_points = detectable_points
        self.monitor = monitor

        # Graphics atributes
        self.triangle = translate_figure(TRIANGLE, (self.x+1, self.y))
        self.triangle = rotate_figure(self.triangle, self.initial_orientation, (self.x, self.y))

        # Threads atributes
        self._stop_event = Event()

    # Thread methods
    def run(self):
        while not self._stop_event.is_set():
            self.update()
            self.detect(self.detectable_points)
            sleep(self.increment/(360*self.revolutions_per_second))

    def stop(self):
        self._stop_event.set()


    # Radar methods
    def _in_sector(self, point: Point, sector: float) -> bool:
        angle = self._angle(point)
        return abs(sector - angle) < self.increment/2

    def _angle(self, point: Point):
        return (math.degrees(
            math.atan2(point.y - self.y, point.x - self.x)) + 360) % 360

    def _distance(self, point: Point) -> float:
        return math.hypot(point.x - self.x, point.y - self.y)

    def update(self):
        self.facing = (self.facing + self.increment) % 360
        self.detection = self.detection_range

    def detect(self, points: list[Point]):
        # determine sector
        sector = (self.initial_orientation + self.facing) % 360
        distances_detected = set()
        for point in points:
            if self._in_sector(point, sector):
                distance = self._distance(point)
                if self.detection_range >= distance:
                    distances_detected.add(distance)

        for distance in distances_detected:
            coordinates = self.get_cartesian_coords(distance, self.facing)
            radar_detection = RadarDetection(
                radar=self,
                distance=distance,
                facing=self.facing,
                x=coordinates[0],
                y=coordinates[1],
            )
            self.detections.add(radar_detection)
            self.monitor.update(detection=radar_detection)
            # print(f"Detección: {radar_detection}")


    # PG1 methods
    def get_cartesian_coords(self, distance: float, angle: float) -> tuple[float, float]:
        x_relative: float = distance * math.cos(math.radians(angle + self.initial_orientation))
        y_relative: float = distance * math.sin(math.radians(angle + self.initial_orientation))
        return self.x + x_relative, self.y + y_relative


    # Visualization methods
    def facing_point(self):
        """
        Return two points making a line where the radar is facing (counting the
        orientation)
        """
        orientation_rad = math.radians(self.initial_orientation + self.facing)
        l = 3
        p1 = (self.x, self.y)
        p2 = (self.x + l * math.cos(orientation_rad), self.y + l * math.sin(orientation_rad))

        return [p1, p2]

    def detection_line(self):
        orientation_rad = math.radians(self.initial_orientation + self.facing)
        l = self.detection
        p1 = (self.x, self.y)
        p2 = (self.x + l * math.cos(orientation_rad), self.y + l * math.sin(orientation_rad))
        return [p1, p2]

    def detection_area(self):
        orientation_rad = math.radians(self.initial_orientation + self.facing)
        half_increment = math.radians(self.increment/2)
        p1 = (self.x + self.detection_range * math.cos(orientation_rad + half_increment), self.y + self.detection_range * math.sin(orientation_rad + half_increment))
        p2 = (self.x + self.detection_range * math.cos(orientation_rad - half_increment), self.y + self.detection_range * math.sin(orientation_rad - half_increment))
        return [p1, p2, (self.x, self.y)]
