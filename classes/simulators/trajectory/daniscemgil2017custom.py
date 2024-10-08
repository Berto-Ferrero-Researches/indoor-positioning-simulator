# Copyright 2024 Alberto Ferrero López
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from classes.simulators.trajectory.interface import TrajectoryInterface
import numpy as np
import random


class DanisCemgil2017Custom(TrajectoryInterface):
    '''
    Custom version of the DanisCemgil2017 class
    This class keeps the same functionality as the original DanisCemgil2017 class, but with some additional features
    It retains the angle constant for a certain amount of time in order to avoid chaotic behavior

    Parameters:
    - keep_angle_ms (int): The duration in milliseconds for which the angle is kept constant.
    - s (float): The standard deviation of the normal distribution used to randomize the angle. A value of 0 means no variance in the angle.

    Attributes:
    - s (float): The standard deviation of the normal distribution used to randomize the angle.
    - outbounds_ration (float): The additional value of π/8 added to the sampled rotation values to prevent the simulation from leaving the area.
    - keep_angle_ms (int): The duration in milliseconds for which the angle is kept constant.

    '''

    def __init__(self, keep_angle_ms: int = 300, s: float = 0.07):
        # Inicialización de variables
        # desviación estandar de la distribución normal usada para aleatorizar el ángulo. 0 = no hay varianza en el ángulo
        self.s = s
        # To prevent our simulation from leaving the area, sampled rotation values are deliberately manipulated by an additional value of π/8 according to the current orientation
        self.outbounds_ration = np.pi / 8   
        # In order to avoid the simulation from being too chaotic, the angle is kept constant for x ms
        self.keep_angle_ms = keep_angle_ms
        self._last_angle_change_time = 0

    def calculate_position(self, current_time: int, milliseconds_per_iteration: int, last_angle: float, last_x: float, last_y: float, min_x: float, max_x: float, min_y: float, max_y: float, speed: float) -> tuple:
        """
        Calculate the new position and angle of a moving object based on the given parameters.
        Parameters:
        - current_time (int): The current time in milliseconds.
        - milliseconds_per_iteration (int): The time elapsed per iteration in milliseconds.
        - last_angle (float): The last recorded angle of movement in radians.
        - last_x (float): The last recorded x-coordinate.
        - last_y (float): The last recorded y-coordinate.
        - min_x (float): The minimum x-coordinate boundary.
        - max_x (float): The maximum x-coordinate boundary.
        - min_y (float): The minimum y-coordinate boundary.
        - max_y (float): The maximum y-coordinate boundary.
        - speed (float): The speed of the moving object in meters per second.
        Returns:
        - tuple: A tuple containing the new x-coordinate, y-coordinate, and angle (x, y, angle).
        """
        x = last_x
        y = last_y

        # Calculamos el angulo de avance
        # Manipulación del valor de rotación para mantener al dispositivo movil dentro del área
        delta_angle = 0
        if x < min_x or x > max_x or y < min_y or y > max_y:
            delta_angle = self.outbounds_ration
            self._last_angle_change_time = current_time # Reset the timer to avoid changing the angle just after the simulator joins the area
        # If we are in the area and the it is the time to change the angle
        elif current_time - self._last_angle_change_time > self.keep_angle_ms:
            # ̃δθ_t ∼ N(0, s)
            delta_angle = np.random.normal(0, self.s)
            self._last_angle_change_time = current_time

        angle = last_angle + delta_angle

        # Calculamos la distancia recorrida
        # velocidad en m/s * tiempo en segundos = distancia recorrida en metros
        delta_l = speed * milliseconds_per_iteration / 1000

        # Incrementamos posiciones
        # x_t = x_(t−1) +  ̃δl_t cos(θ_(t−1) +  ̃δθ_t)
        x += delta_l * np.cos(angle)
        # y_t = y_(t−1) +  ̃δl_t sin(θ_(t−1) +  ̃δθ_t)
        y += delta_l * np.sin(angle)

        # Devolvemos
        return (x, y, angle)
