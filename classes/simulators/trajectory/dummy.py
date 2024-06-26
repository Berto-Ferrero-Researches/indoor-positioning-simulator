from classes.simulators.trajectory.interface import TrajectoryInterface
import random

class DummyPositionModule(TrajectoryInterface):

    def calculate_position(self, current_time: int, milliseconds_per_iteration: int, last_angle: float, last_x: float, last_y: float, min_x: float, max_x: float, min_y: float, max_y: float, speed: float) -> tuple:
        return (random.uniform(min_x, max_x), random.uniform(min_y, max_y))