# external imports
from time import sleep
import matplotlib.pyplot as plt
import os
# internal imports
from src.actors.points.circular_point import CircularPoint
from src.actors.points.eight_point import EightPoint
from src.actors.points.path_point import PathPoint
from src.actors.radar import Radar
from src.base.monitor import Monitor
from src.base.lector import Lector
from src.graphics.map_view import MapView


if __name__ == '__main__':
    # Constants
    AREA = 200
    EXECUTING_SECONDS = 30
    MAIN_DIR = os.path.dirname(os.path.abspath(__file__))

    # Create figures for graphics
    fig = plt.figure(1, figsize=(10, 10))
    axe_map= fig.subplots(nrows=1, ncols=1)

    # Create monitors and lectors
    number_of_monitors = 2
    monitors = []
    lectors = []
    for index in range(number_of_monitors):
        monitors.append(Monitor())
        lectors.append(Lector(
            monitor=monitors[index]
        ))

    # Create points
    points = [
        EightPoint(x=100, y=100),
        CircularPoint(x=40, y=140, radius=25),
        CircularPoint(x=140, y=40, radius=25),
        # PathPoint(
        #     x=100,
        #     y=100,
        #     svg_path_file=f"{MAIN_DIR}/src/svg_images/star.svg"
        # ),
    ]

    # Create radars
    radars = [
        Radar(name="radar0",
              position=(50,100),
              detection_range=50,
              orientation_initial=180,
              increment=90,
              revolutions_per_second=2,
              detectable_points=points,
              monitor=monitors[0]),
        Radar(name="radar1",
              position=(150,100),
              detection_range=50,
              orientation_initial=0,
              increment=90,
              revolutions_per_second=2,
              detectable_points=points,
              monitor=monitors[0]),
        Radar(name="radar2",
              position=(100,50),
              detection_range=50,
              orientation_initial=270,
              increment=90,
              revolutions_per_second=2,
              detectable_points=points,
              monitor=monitors[1]),
        Radar(name="radar3",
              position=(100,150),
              detection_range=50,
              orientation_initial=90,
              increment=90,
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

    view = MapView(height=AREA, width=AREA, axes=axe_map)
    view.animate(radars, points, interval=30)
    plt.show()

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
