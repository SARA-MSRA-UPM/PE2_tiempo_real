# external imports
# internal imports


class RadarDetection:
    def __init__(
            self,
            radar,
            distance: float,
            facing: float,
            x: float,
            y: float,
        ):
        self.radar = radar
        self.distance = distance
        self.facing = facing
        self.x = x
        self.y = y

    def __repr__(self):
        return ("RadarDetection("
            f"radar={self.radar.name}, "
            f"distance={self.distance}, "
            f"facing={self.facing}, "
            f"coords=[{self.x}, {self.y}]"
            ")")
