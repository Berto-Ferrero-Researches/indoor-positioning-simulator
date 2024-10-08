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

import json
import os

import numpy as np


class Config:
    """
    Config class for loading, extracting, and validating simulation configuration parameters.
    Attributes:
        simulation_duration_seconds (int): Duration of the simulation in seconds.
        room_dim_meters (dict): Dimensions of the room in meters.
        margin_meters (float): Margin in meters.
        initial_position (dict): Initial position with 'x' and 'y' coordinates.
        speed_meters_second (float): Speed in meters per second.
        initial_angle_degrees (float): Initial angle in degrees.
        output_trajectory (bool): Indicates if the trajectory is going to be registered.
        trajectory_simulator_module (str): Name of the trajectory simulator module.
        trajectory_simulator_parameters (dict): General configuration for all possible modules.
        trajectory_simulator_module_parameters (dict): Specific configuration for the selected trajectory module.
        rssi_simulator_module (str): Name of the RSSI simulator module.
        rssi_simulator_parameters (dict): General configuration for all possible RSSI modules.
        rssi_simulator_module_parameters (dict): Specific configuration for the selected RSSI module.
    """
    def __init__(self, config_path):
        # Load the configuration file
        config = self._load_config_file(config_path)
        
        # Extract and store localy all the required configuration parameters
        self._extract_config_parameters(config)

        # Validate the configuration
        self._validate_config()

    def _extract_config_parameters(self, config: dict):
        """
        Extracts the configuration parameters from the given dictionary and assigns them to the corresponding attributes.

        Args:
            config (dict): The dictionary containing the configuration parameters.

        Returns:
            None
        """
        # General parameters
        self.simulation_duration_seconds = config.get('simulation_duration_seconds', 60)
        self.room_dim_meters = config.get('room_dim_meters', None)
        self.margin_meters = config.get('margin_meters', 0)
        self.initial_position = config.get('initial_position', {'x': 0, 'y': 0})
        self.speed_meters_second = config.get('speed_meters_second', 0.5)
        self.initial_angle_degrees = config.get('initial_angle_degrees', np.random.uniform(0, 360))
        self.output_trajectory = config.get('output_trajectory', True) #Indicates if the trajectory is going to be registered (csv extracted and plotted)

        # Simulator modules parameters
        simulators = config.get('simulators', {})
        
        self.trajectory_simulator_module = simulators.get('trajectory', "")
        self.trajectory_simulator_parameters = simulators.get('trajectory_parameters', {}) #Configuración general de todos los posibles modulos
        self.trajectory_simulator_module_parameters = self.trajectory_simulator_parameters.get(self.trajectory_simulator_module, {}) #Configuración específica del módulo seleccionado

        self.rssi_simulator_module = simulators.get('rssi', "")
        self.rssi_simulator_parameters = simulators.get('rssi_parameters', {})
        self.rssi_simulator_module_parameters = self.rssi_simulator_parameters.get(self.rssi_simulator_module, {})

    def _validate_config(self):
        """
        Validates the configuration parameters for the simulation.
        Raises:
            ValueError: If any of the configuration parameters are invalid.
        Validations:
            - Simulation duration must be greater than 0.
            - Room dimensions must be provided and include 'x' and 'y' indices.
            - Room dimensions must be greater than 0.
            - Margin must be greater or equal to 0.
            - Initial position must include 'x' and 'y' indices and be greater or equal to 0.
            - Speed must be greater than 0.
            - Initial angle must be between 0 and 360 degrees.
            - Trajectory simulator module must be provided.
            - RSSI simulator module must be provided.
            - Initial position must be within the bounds of the room dimensions considering the margin.
        """

        # Basic parameters restrictions
        if self.simulation_duration_seconds <= 0:
            raise ValueError("Simulation duration must be greater than 0.")
        
        if self.room_dim_meters is None:
            raise ValueError("Room dimensions must be provided.")
        if 'x' not in self.room_dim_meters or 'y' not in self.room_dim_meters:
            raise ValueError("Room dimensions must include 'x' and 'y' indices.")
        if self.room_dim_meters.get('x', 0) <= 0 or self.room_dim_meters.get('y', 0) <= 0:
            raise ValueError("Room dimensions must be greater than 0.")
        
        if self.margin_meters < 0:
            raise ValueError("Margin must be greater or equal to 0.")
        
        if 'x' not in self.initial_position or 'y' not in self.initial_position:
            raise ValueError("Initial position must include 'x' and 'y' indices.")
        if self.initial_position.get('x', 0) < 0 or self.initial_position.get('y', 0) < 0:
            raise ValueError("Initial position must be greater or equal to 0.")
        
        if self.speed_meters_second <= 0:
            raise ValueError("Speed must be greater than 0.")
        
        if self.initial_angle_degrees < 0 or self.initial_angle_degrees >= 360:
            raise ValueError("Initial angle must be between 0 and 360 degrees.")
        
        if not self.trajectory_simulator_module:
            raise ValueError("Trajectory simulator module must be provided.")
        
        if not self.rssi_simulator_module:
            raise ValueError("RSSI simulator module must be provided.")


        # Room size coherence
        if self.initial_position['x'] < self.margin_meters or self.initial_position['x'] > self.room_dim_meters['x'] - self.margin_meters:
            raise ValueError("Initial x position is out of bounds.")
        if self.initial_position['y'] < self.margin_meters or self.initial_position['y'] > self.room_dim_meters['y'] - self.margin_meters:
            raise ValueError("Initial y position is out of bounds.")
           

    def _load_config_file(self, config_path: str) -> dict:
        """
        Load the configuration file from the given path and return it as a dictionary.

        Args:
            config_path (str): The path to the configuration file.

        Returns:
            dict: The loaded configuration as a dictionary.

        Raises:
            FileNotFoundError: If the config file does not exist.
            ValueError: If the config file has an invalid format.
        """
        # First check if the config file exists
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file {config_path} not found")

        # Load the config file as json file
        with open(config_path, 'r') as file:
            config = json.load(file)

        # Check if the config file was loaded correctly
        if not isinstance(config, dict):
            raise ValueError("Invalid config file format.")
        
        return config