from sat_controller import SatControllerInterface, sat_msgs

# Team code is written as an implementation of various methods
# within the the generic SatControllerInterface class.

# Specifically, init, run, abort and reset

class TeamController(SatControllerInterface):

    def team_init(self):
        # Run any initialization you need

        # Example of persistant data
        self.counter = 0

        # Example of logging
        self.logger.info("Initialized :)")
        self.logger.warning("Warning...")
        self.logger.error("Error!")

        # Update team info
        team_info = sat_msgs.TeamInfo()
        team_info.teamName = "Example"
        team_info.teamID = 1111

        # Return team info
        return team_info

    def team_run(self, system_state: sat_msgs.SystemState, satellite_state: sat_msgs.SataliteState) -> sat_msgs.ControlMessage:

        # Get timedelta from elapsed time
        elapsed_time = system_state.elapsedTime.ToTimedelta()
        self.logger.info(f'Elapsed time: {elapsed_time}')

        # Example of persistant data
        self.counter += 1

        # Example of logging
        self.logger.info(f'Counter value: {self.counter}')

        # Create a thrust command message
        thrust_cmd = sat_msgs.ControlMessage()

        # Set thrust command values
        if(elapsed_time.total_seconds() < 1.5):
            thrust_cmd.thrust.f_x = 0.5
        else:
            thrust_cmd.thrust.f_x = -2.0 * (satellite_state.pose.x - 2) - 3.0 * satellite_state.twist.v_x
            thrust_cmd.thrust.f_y = -2.0 * (satellite_state.pose.y - 4 - 0.3) - 3.0 * satellite_state.twist.v_y
            thrust_cmd.thrust.tau = -2.0 * (satellite_state.pose.theta + 2 - 3.1415) - 3.0 * satellite_state.twist.omega

        # Return thrust command
        return thrust_cmd

    def team_reset(self) -> None:
        # Run any reset code
        pass