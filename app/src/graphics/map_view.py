# external imports
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.artist import Artist
from matplotlib.patches import Polygon
# internal imports
from ..actors.radar import Radar


class MapView:
    def __init__(self, width: int, height: int, axes: plt.Axes):
        self._width = width
        self._height = height
        self._axes = axes

    def init_plot(self) -> list[Artist] | None:
        """
        Initializes the plot by setting limits and static features.
        """
        self._axes.set_xlim(0, self._width)
        self._axes.set_ylim(0, self._height)
        return None

    def update(self, frame, radars, points):
        """
        Updates the radar and points for each frame of the animation.
        """
        self._axes.clear()  # Clear the axes for the new frame
        self._axes.set_xlim(0, self._width)
        self._axes.set_ylim(0, self._height)

        for radar in radars:
            self._draw_radar_and_detection_range(radar)
            self._draw_orientation_triangle(radar.triangle)
            self._draw_radar_facing_direction(radar)
            self._draw_radar_detection_area(radar)
            self._draw_detection_line(radar)

        # Draw points
        for point in points:
            self._axes.plot(point.x, point.y, 'ro')

    def _draw_radar_and_detection_range(self, radar: Radar):
        self._axes.plot(radar.x, radar.y, 'go')
        self._axes.add_artist(
            plt.Circle(
                xy=(radar.x, radar.y),
                radius=radar.detection_range,
                color='g',
                fill=False)
        )

    def _draw_orientation_triangle(self, triangle):
        """
        Draws the radar's orientation triangle.
        """
        triangle_patch = Polygon(triangle, color='blue', alpha=0.5)
        self._axes.add_patch(triangle_patch)

    def _draw_radar_facing_direction(self, radar: Radar):
        facing = radar.facing_point()
        self._axes.plot([radar.x, facing[1][0]], [radar.y, facing[1][1]], 'g-')

    def _draw_radar_detection_area(self, radar: Radar):
        self._axes.add_patch(
            Polygon(radar.detection_area(), color='g', alpha=0.1)
        )

    def _draw_detection_line(self, radar: Radar):
        if radar.detection < radar.detection_range:
            detected_pos = radar.detection_line()
            self._axes.plot(
                [radar.x, detected_pos[1][0]],
                [radar.y, detected_pos[1][1]],
                'r-'
            )

    def animate(self, radars, points, interval=100):
        """
        Creates the animation using FuncAnimation.
        """
        # Create the FuncAnimation object
        self.ani = FuncAnimation(
            fig=self._axes.figure,
            func=self.update,
            fargs=(radars, points),
            init_func=self.init_plot,
            interval=interval,
            save_count=300
        )

    def save_animation(self, filename, radars, points, interval=100):
        """
        Saves the animation as a GIF file.
        :param filename: The name of the GIF file to save.
        :param radars: List of radars.
        :param points: List of points.
        :param interval: Time interval between frames (in ms).
        """

        self.ani.save(filename, writer='pillow', fps=30)