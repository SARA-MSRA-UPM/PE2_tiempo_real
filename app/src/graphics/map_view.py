# external imports
from matplotlib.widgets import TextBox
import matplotlib.pyplot as plt
from re import match
from turtledemo.paint import switchupdown

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.artist import Artist
from matplotlib.patches import Polygon
# internal imports
from ..actors.radar import Radar
from ..helpers.helpers import radar_detection_to_point
from ..actors.points.point import Point

class MapView:
    def __init__(self, width: int, height: int, axes: plt.Axes, axes_bis: plt.Axes, fig: plt.Figure):
        self._width = width
        self._height = height
        self._axes = axes
        self._axes_bis = axes_bis
        self._fig = fig

        # Imprimir las detecciones
        self._cont0 = 0
        self._cont1 = 0
        self._cont2 = 0
        self._cont3 = 0
        self._contCom = 0

        self._txtBoxTitle0 = self._fig.text(
            0.1, 0.05, "Radar 0:",
            ha='center', va='center', fontsize=12, color='red'
        )
        self._txtBox0 = self._fig.text(
        0.15, 0.05, f"{self._cont0}",
        ha='center', va='center', fontsize=12, color='red',
        bbox=dict(facecolor='lightgray', edgecolor='black', boxstyle='round,pad=0.5', linewidth=1.5)
        )
        self._txtBoxTitle1 = self._fig.text(
            0.23, 0.05, "Radar 1:",
            ha='center', va='center', fontsize=12, color='blue'
        )
        self._txtBox1 = self._fig.text(
            0.28, 0.05, f"{self._cont1}",
            ha='center', va='center', fontsize=12, color='blue',
            bbox=dict(facecolor='lightgray', edgecolor='black', boxstyle='round,pad=0.5', linewidth=1.5)
        )
        self._txtBoxTitle2 = self._fig.text(
            0.35, 0.05, "Radar 2:",
            ha='center', va='center', fontsize=12, color='black'
        )
        self._txtBox2 = self._fig.text(
            0.40, 0.05, f"{self._cont2}",
            ha='center', va='center', fontsize=12, color='black',
            bbox=dict(facecolor='lightgray', edgecolor='black', boxstyle='round,pad=0.5', linewidth=1.5)
        )
        self._txtBoxTitle3 = self._fig.text(
            0.47, 0.05, "Radar 3:",
            ha='center', va='center', fontsize=12, color='yellow'
        )
        self._txtBox3 = self._fig.text(
            0.52, 0.05, f"{self._cont3}",
            ha='center', va='center', fontsize=12, color='yellow',
            bbox=dict(facecolor='lightgray', edgecolor='black', boxstyle='round,pad=0.5', linewidth=1.5)
        )
        self._txtBoxTitleCom = self._fig.text(
            0.59, 0.05, "Common:",
            ha='center', va='center', fontsize=12, color='magenta'
        )
        self._txtBoxCom = self._fig.text(
            0.64, 0.05, f"{self._cont3}",
            ha='center', va='center', fontsize=12, color='magenta',
            bbox=dict(facecolor='lightgray', edgecolor='black', boxstyle='round,pad=0.5', linewidth=1.5)
        )

        # Add graphic title
        self._axes_bis.set_title("Detections")

    def init_plot(self) -> list[Artist] | None:
        """
        Initializes the plot by setting limits and static features.
        """
        self._axes.set_xlim(0, self._width)
        self._axes.set_ylim(0, self._height)
        self._axes_bis.set_xlim(0, self._width)
        self._axes_bis.set_ylim(0, self._height)
        return None

    def update(self, frame, radars, points):
        """
        Updates the radar and points for each frame of the animation.
        """
        self._axes.clear()  # Clear the axes for the new frame
        self._axes.set_xlim(0, self._width)
        self._axes.set_ylim(0, self._height)
        self._axes.set_title("Map View")

        # Añadir líneas a la leyenda
        line1 = plt.Line2D([0], [0], color='red', lw=2, label='Radar 0')
        line2 = plt.Line2D([0], [0], color='blue', lw=2, label='Radar 1')
        line3 = plt.Line2D([0], [0], color='black', lw=2, label='Radar 2')
        line4 = plt.Line2D([0], [0], color='yellow', lw=2, label='Radar 3')
        self._axes.legend(handles=[line1, line2, line3, line4])

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
        color_radar = 'b'
        match radar.name:
            case "radar0":
                color_radar = 'r'
            case "radar1":
                color_radar = 'b'
            case "radar2":
                color_radar = 'k'
            case "radar3":
                color_radar = 'y'

        self._axes.add_artist(
            plt.Circle(
                xy=(radar.x, radar.y),
                radius=radar.detection_range,
                color=color_radar,
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

    def draw_detected_point(self, point: Point, detection_radar: str):

        match detection_radar:
            case "radar0":
                self._axes_bis.plot(point.x, point.y, 'rx')
                self._cont0 += 1
            case "radar1":
                self._axes_bis.plot(point.x, point.y, 'bx')
                self._cont1 += 1
            case "radar2":
                self._axes_bis.plot(point.x, point.y, 'kx')
                self._cont2 += 1
            case "radar3":
                self._axes_bis.plot(point.x, point.y, 'yx')
                self._cont3 += 1
            case "cds":
                self._axes_bis.plot(point.x, point.y, 'mo')
                self._contCom += 1

        self._txtBox0.set_text(f"{self._cont0}")
        self._txtBox1.set_text(f"{self._cont1}")
        self._txtBox2.set_text(f"{self._cont2}")
        self._txtBox3.set_text(f"{self._cont3}")
        self._txtBoxCom.set_text(f"{self._contCom}")

