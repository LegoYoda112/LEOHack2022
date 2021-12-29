from sat_controller import SatControllerInterface, sat_msgs

# Team code is written as an implementation of various methods
# within the the generic SatControllerInterface class.

# Specifically, init, run, abort and reset

class TeamController(SatControllerInterface):

    def init(self):
        # Run any initialization you need

        # Example of persistant data
        self.counter = 0

        # Example of logging
        self.logger.info("Initialized :)")
        self.logger.warning("Warning...")
        self.logger.error("Error!")

        # Update team info
        team_info = sat_msgs.TeamInfo()
        team_info.teamName = "Example team"
        team_info.teamID = 1111

        # Return team info
        return team_info

    def run(self, system_state: sat_msgs.SystemState, satellite_state: sat_msgs.SataliteState) -> sat_msgs.ThrustCommand:
        
        # Example of persistant data
        self.counter += 1

        # Example of logging
        self.logger.info(f'Counter value: {self.counter}')

        # Create a thrust command message
        thrust_cmd = sat_msgs.ThrustCommand()

        # Set thrust command values
        thrust_cmd.thrust.f_x = 0.0
        thrust_cmd.thrust.f_y = 0.0
        thrust_cmd.thrust.tau = 0.0
        return thrust_cmd

    def abort(self) -> None:
        # Run any abort code
        pass

    def reset(self) -> None:
        # Run any reset code
        pass