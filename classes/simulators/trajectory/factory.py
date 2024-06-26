from classes.simulators.trajectory.interface import TrajectoryInterface

class TrajectoryFactory:
    """
    A factory class for creating trajectory simulators.
    """

    @staticmethod
    def create_trajectory_simulator(simulator_name: str) -> TrajectoryInterface:
        """
        Creates a trajectory simulator based on the given simulator name.

        Args:
            simulator_name (str): The name of the simulator.

        Returns:
            TrajectoryInterface: An instance of the trajectory simulator.

        Raises:
            ValueError: If the simulator name is not available.
        """
        if simulator_name == 'dummy':
            from classes.simulators.trajectory.dummy import DummyPositionModule
            return DummyPositionModule()
        elif simulator_name == 'daniscemgil2017':
            from classes.simulators.trajectory.daniscemgil2017 import DanisCemgil2017
            return DanisCemgil2017()
        elif simulator_name == 'daniscemgil2017custom':
            from classes.simulators.trajectory.daniscemgil2017custom import DanisCemgil2017Custom
            return DanisCemgil2017Custom()
        else:
            raise ValueError(f"Trajectory simulator {simulator_name} not available.")
