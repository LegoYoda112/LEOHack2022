import math

from sat_controller import SatControllerInterface, sat_msgs

# Team code is written as an implementation of various methods
# within the the generic SatControllerInterface class.
# If you would like to see how this class works, look in sat_control/sat_controller

# Specifically, init, run, and reset

class TeamController(SatControllerInterface):
    """ Team control code """

    def team_init(self):
        """ Runs any team based initialization """
        # Run any initialization you need
        self.set_mass(1)
        self.set_inertia(1)

        # Example of persistant data
        self.counter = 0

        # Example of logging
        self.logger.info("Initialized :)")
        self.logger.warning("Warning...")
        self.logger.error("Error!")

        # Update team info
        team_info = sat_msgs.TeamInfo()
        team_info.teamName = "FakeNASA"
        team_info.teamID = 6969

        # Return team info
        return team_info

    def team_run(self, system_state: sat_msgs.SystemState, satellite_state: sat_msgs.SatelliteState, dead_sat_state: sat_msgs.SatelliteState) -> sat_msgs.ControlMessage:
        """ Takes in a system state, satellite state """

        print(dead_sat_state)
        print(satellite_state)
        print(satellite_state.fuel)
        print(f'Mass: {self.sat_description.mass}')

        # Get timedelta from elapsed time
        elapsed_time = system_state.elapsedTime.ToTimedelta()
        self.logger.info(f'Elapsed time: {elapsed_time}')

        # Example of persistant data
        self.counter += 1

        # Example of logging
        self.logger.info(f'Counter value: {self.counter}')

        # Create a thrust command message
        control_message = sat_msgs.ControlMessage()

        # Defining target position, damping, k
        x_target = dead_sat_state.pose.x + 0.25 * math.cos(dead_sat_state.pose.theta - math.pi / 2)
        y_target = dead_sat_state.pose.y + 0.25 * math.sin(dead_sat_state.pose.theta - math.pi / 2)

        displacement_x = satellite_state.pose.x - dead_sat_state.pose.x
        displacement_y = satellite_state.pose.y - dead_sat_state.pose.y
        displacement = math.sqrt(displacement_x ** 2 + displacement_y ** 2)

        if displacement > 0.5:
            k_x = (math.e/2.03576)**2
            k_y = (math.e/-0.81430)**2
        else:
            k_x = (0.2/(0.5-x_target))**2
            k_y = (0.2/(0.5-y_target))**2

        crit_damp_x = 2 * math.sqrt(self.sat_description.mass * k_x)
        crit_damp_y = 2 * math.sqrt(self.sat_description.mass * k_y)

        # Set thrust command values, basic PD controller that drives the sat to [0, -1]
        control_message.thrust.f_x = -k_x * (satellite_state.pose.x - ((x_target-1.5)*2 + 1.5)) - crit_damp_x * satellite_state.twist.v_x
        control_message.thrust.f_y = -k_y * (satellite_state.pose.y - ((y_target-(-2))*2 - 2)) - crit_damp_y * satellite_state.twist.v_y
        control_message.thrust.tau = -k_y * (satellite_state.pose.theta - (dead_sat_state.pose.theta) - (math.pi / 3)) - crit_damp_y * satellite_state.twist.omega

        # control_message.thrust.f_x = -k * (satellite_state.pose.x - (x_target)) - crit_damp * satellite_state.twist.v_x
        # control_message.thrust.f_y = -k * (satellite_state.pose.y - (y_target)) - crit_damp * satellite_state.twist.v_y
        # control_message.thrust.tau = -k * (satellite_state.pose.theta - (dead_sat_state.pose.theta) - (math.pi / 3)) - crit_damp * satellite_state.twist.omega

        displacement_x = satellite_state.pose.x - dead_sat_state.pose.x
        displacement_y = satellite_state.pose.y - dead_sat_state.pose.y
        displacement = math.sqrt(displacement_x**2 + displacement_y**2)
        vel = math.sqrt(satellite_state.twist.v_x**2 + satellite_state.twist.v_y**2)
        if displacement < 0.5:
            print("VELOCITY:", vel)
            if vel > 0.2:
                print("FAIL")
            else:
                print("WORKSSS")
        print("displacement:", displacement)
        print("velocity:", vel)

        # Return control message
        return control_message

    def team_reset(self) -> None:
        # Run any reset code
        pass