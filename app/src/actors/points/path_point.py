# external imports
from svgpathtools import svg2paths
# internal imports
from .point import Point


class PathPoint(Point):

    def __init__(self,
                 x: float,
                 y: float,
                 svg_path_file: str,
                 speed: float=0.1):
        """
        Initialize a point that follows a path extracted from an SVG file.
        :param svg_path_file: Path to the SVG file containing the path.
        :param speed: Speed at which the point moves along the path (fraction between points).
        """
        super().__init__(x, y)
        self.path_points = self._extract_path(svg_path_file)
        self.path_index = 0
        # Parameter to track interpolation progress between points
        self.t = 0
        # Speed controls how quickly it moves between points
        self.speed = speed
        self.update()

    def _extract_path(self, svg_path_file):
        """
        Extracts the path points from the SVG file.
        :param svg_path_file: Path to the SVG file.
        :return: A list of (x, y) coordinates representing the path.
        """
        paths, _ = svg2paths(svg_path_file)
        points = []

        # Sample the path at regular intervals (based on length)
        for path in paths:
            num_points = 100  # Adjust this number to control path resolution
            for i in range(num_points):
                t = i / num_points
                point = path.point(t)
                points.append((point.real, point.imag))  # real is x, imag is y
        return points

    def _interpolate(self,
                     p1: tuple[float, float],
                     p2: tuple[float, float],
                     t: float):
        """
        Linear interpolation between two points.
        :param p1: The first point (x1, y1).
        :param p2: The second point (x2, y2).
        :param t: A parameter between 0 and 1 that interpolates between p1 and p2.
        :return: Interpolated (x, y) position.
        """
        x1, y1 = p1
        x2, y2 = p2
        x = x1 + t * (x2 - x1)
        y = y1 + t * (y2 - y1)
        return x, y

    def update(self):
        """
        Moves along the SVG path incrementally with interpolation.
        """
        if self.path_index < len(self.path_points) - 1:
            p1 = self.path_points[self.path_index]
            p2 = self.path_points[self.path_index + 1]

            # Interpolate between points
            self.x, self.y = self._interpolate(p1, p2, self.t)

            # Increment t by speed; if t >= 1, move to the next segment
            self.t += self.speed
            if self.t >= 1:
                self.t = 0
                self.path_index += 1
        else:
            # If the path is completed, loop back to the start
            self.path_index = 0
            self.t = 0