from sat_controller import SatControllerInterface, sat_msgs

class TeamController(SatControllerInterface):

    def run(self, system_state: sat_msgs.SystemState, satellite_state: sat_msgs.SataliteState) -> sat_msgs.ThrustCommand:
        
        # Create a thrust command message
        thrust_cmd = sat_msgs.ThrustCommand()

        # Set thrust command values
        thrust_cmd.thrust.f_x = 0.0
        thrust_cmd.thrust.f_y = 0.0
        thrust_cmd.thrust.tau = 0.0
        return thrust_cmd

    def init(self):
        # Run any initialization you need

        # Update team info
        team_info = sat_msgs.TeamInfo()
        team_info.teamName = "Example team"
        team_info.teamID = 1111

        # Return team info
        return team_info

    def abort(self) -> None:
        # Run any abort code
        pass

    def reset(self) -> None:
        # Run any reset code
        pass

test_team_controller = TeamController()
print(test_team_controller.init())