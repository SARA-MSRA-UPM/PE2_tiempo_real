# external imports
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Polygon
import math
# internal imports
from src.actors.radar import Radar
from src.actors.points.point import Point    

class MapView:
    def __init__(
            self,
            width: int,
            height: int,
            axes: plt.axes,
            title: str = "MapView"):
        self.width = width
        self.height = height
        self.axes = axes

    def init_plot(self):
        """
        Initializes the plot by setting limits and static features.
        """
        self.axes.set_xlim(0, self.width)
        self.axes.set_ylim(0, self.height)

    def animate(self, radars, points, interval=100):
        """
        Creates the animation using FuncAnimation.
        """
        # Create the FuncAnimation object
        self.animation = FuncAnimation(
            self.axes.figure, 
            self.update, 
            fargs=(radars, points),
            init_func=self.init_plot, 
            interval=interval,
            save_count=300
        )

    def update(self, frame, radars: list[Radar], points: list[Point]):
        """
        Updates the radar and points for each frame of the animation.
        """
        self.axes.clear()  # Clear the axes for the new frame
        self.axes.set_xlim(0, self.width)
        self.axes.set_ylim(0, self.height)
        
        for radar in radars:
            # Draw radar position and detection range
            self.axes.plot(radar.x, radar.y, 'go')
            circle = plt.Circle((radar.x, radar.y), radar.detection_range, color='g', fill=False)
            self.axes.add_artist(circle)
            
            # Draw radar orientation triangle
            self._draw_orientation_triangle(radar.triangle)
            
            # Draw the radar's facing direction
            facing = radar.facing_point()
            self.axes.plot([radar.x, facing[1][0]], [radar.y, facing[1][1]], 'g-')
            
            # Draw the radar's detection area
            self.axes.add_patch(Polygon(radar.detection_area(), color='g', alpha=0.1))
            
            # Draw detection line if something is detected
            if radar.detection < radar.detection_range:
                detected_pos = radar.detection_line()
                self.axes.plot([radar.x, detected_pos[1][0]], [radar.y, detected_pos[1][1]], 'r-')

        # Draw points
        for point in points:
            self.axes.plot(point.x, point.y, 'ro')

    def _draw_orientation_triangle(self, triangle):
        """
        Draws the radar's orientation triangle.
        """
        triangle_patch = Polygon(triangle, color='blue', alpha=0.5)
        self.axes.add_patch(triangle_patch)

