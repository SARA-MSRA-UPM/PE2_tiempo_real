# external imports
from time import sleep
import matplotlib.pyplot as plt
# internal imports
from src.actors.points.circular_point import Point
from src.actors.points.circular_point import CircularPoint
from src.actors.points.eight_point import EightPoint
from src.actors.points.path_point import PathPoint
from src.actors.radar import Radar
from src.monitors.detections_monitor import DetectionsMonitor
from src.actors.detections_consumer import DetectionsConsumer
from src.graphics.map_view import MapView


if __name__ == '__main__':
    # Constants
    AREA = 200

    # Creat graphics instances
    fig = plt.figure(1, figsize=(10, 10))
    radars_axes= fig.subplots(nrows=1, ncols=1)
    radars_view = MapView(
        height=AREA,
        width=AREA,
        axes=radars_axes,
        title="Radars View")

    # Create monitors and lectors
    number_of_monitors = 2
    monitors = [] 
    lectors = []
    for index in range(number_of_monitors):
        monitors.append(DetectionsMonitor())
        lectors.append(DetectionsConsumer(
            monitor=monitors[index]
        ))

    # Create points
    points = [
        EightPoint(x=100, y=100),
        CircularPoint(x=40, y=140, radius=25),
        CircularPoint(x=140, y=40, radius=25),
        # Point(x=60, y=60),
        # Point(x=15, y=120),
        # Point(x=120, y=15)
        # PathPoint(x=100, y=100, svg_path_file="./app/sources/star.svg"),
    ]

    # Create radars
    radars = [
        Radar(name="radar0",
              position=(50,100),
              detection_range=50,
              initial_orientation=180,
              increment=15,
              revolutions_per_second=2,
              detectable_points=points,
              monitor=monitors[0]),
        Radar(name="radar1",
              position=(150,100),
              detection_range=50,
              initial_orientation=0,
              increment=15,
              revolutions_per_second=2,
              detectable_points=points,
              monitor=monitors[0]),
        Radar(name="radar2",
              position=(100,50),
              detection_range=50,
              initial_orientation=270,
              increment=15,
              revolutions_per_second=2,
              detectable_points=points,
              monitor=monitors[1]),
        Radar(name="radar3",
              position=(100,150),
              detection_range=50,
              initial_orientation=90,
              increment=15,
              revolutions_per_second=2,
              detectable_points=points,
              monitor=monitors[1]),
    ]

    # Start threads
    for radar in radars:
        radar.start()

    for point in points:
        point.start()

    for lector in lectors:
        lector.start()
   
    # Start the animation
    radars_view.animate(radars, points)
    
    # Show the plot
    plt.show()

    # This part is executed once the graphics are closed
    for lector in lectors:
        lector.stop()
        lector.join()
    print("Lectors stopped")

    # Stop all threads
    for radar in radars:
        radar.stop()
        radar.join()
    print("Radars stopped")

    for point in points:
        point.stop()
        point.join()
    print("Points stopped")

    exit(0)
