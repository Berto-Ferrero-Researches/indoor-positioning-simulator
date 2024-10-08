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

class TrajectoryFactory:
    """
    A factory class for creating trajectory simulators.
    """

    @staticmethod
    def create_trajectory_simulator(simulator_name: str, constructor_params: dict = {}) -> TrajectoryInterface:
        """
        Creates a trajectory simulator based on the given simulator name.

        Args:
            simulator_name (str): The name of the simulator.
            constructor_params (dict): Optional dictionary of constructor parameters.

        Returns:
            TrajectoryInterface: An instance of the trajectory simulator.

        Raises:
            ValueError: If the simulator name is not available.
        """
        if simulator_name == 'dummy':
            from classes.simulators.trajectory.dummy import DummyPositionModule
            return DummyPositionModule(**constructor_params)
        elif simulator_name == 'daniscemgil2017':
            from classes.simulators.trajectory.daniscemgil2017 import DanisCemgil2017
            return DanisCemgil2017(**constructor_params)
        elif simulator_name == 'daniscemgil2017custom':
            from classes.simulators.trajectory.daniscemgil2017custom import DanisCemgil2017Custom
            return DanisCemgil2017Custom(**constructor_params)
        else:
            raise ValueError(f"Trajectory simulator {simulator_name} not available.")
