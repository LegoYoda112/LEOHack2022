from sat_controller import SatControllerInterface, sat_msgs

# Team code is written as an implementation of various methods
# within the the generic SatControllerInterface class.
# If you would like to see how this class works, look in sat_control/sat_controller

# Specifically, init, run, and reset

from math import sin, cos
import math

class TeamController(SatControllerInterface):
    """ Team control code """

    def team_init(self):
        """ Runs any team based initialization """
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

    def team_run(self, system_state: sat_msgs.SystemState, satellite_state: sat_msgs.SatelliteState, dead_sat_state: sat_msgs.SatelliteState) -> sat_msgs.ControlMessage:
        """ Takes in a system state, satellite state """

        print(dead_sat_state)

        # Get timedelta from elapsed time
        elapsed_time = system_state.elapsedTime.ToTimedelta()
        self.logger.info(f'Elapsed time: {elapsed_time}')

        # Example of persistant data
        self.counter += 1

        # Example of logging
        self.logger.info(f'Counter value: {self.counter}')

        # Create a thrust command message
        control_message = sat_msgs.ControlMessage()
<<<<<<< Updated upstream

        # Set thrust command values, basic PD controller that drives the sat to [0, -1]
        control_message.thrust.f_x = -2.0 * (satellite_state.pose.x - (dead_sat_state.pose.x+0.25*cos(dead_sat_state.pose.theta - math.pi / 2))) - 3.0 * satellite_state.twist.v_x
        control_message.thrust.f_y = -2.0 * (satellite_state.pose.y - (dead_sat_state.pose.y+0.25*sin(dead_sat_state.pose.theta - math.pi / 2))) - 3.0 * satellite_state.twist.v_y
        control_message.thrust.tau = -1.5 * (satellite_state.pose.theta - dead_sat_state.pose.theta) - 3.0 * satellite_state.twist.omega
        #print(satellite_state.pose.x)
        #print(satellite_state.pose.y)
        #print(satellite_state.pose.theta)
=======
        
        radius = 0.5
        docking = 0.30

        xdistance = abs(satellite_state.pose.x - dead_sat_state.pose.x)
        ydistance = abs(satellite_state.pose.y - dead_sat_state.pose.y)
        print(satellite_state.twist) 
        print("omega",satellite_state.twist.omega)
        print("distance",sqrt(xdistance**2+ydistance**2))   
        if dead_sat_state.pose.theta>0:
            diversion=1
        elif dead_sat_state.pose.theta<0:
            diversion=-1

        if sqrt(xdistance**2+ydistance**2)<docking: #DOCKING PART
            control_message.thrust.f_x = -30 * (satellite_state.pose.x - ((dead_sat_state.pose.x)+(0.25*cos(dead_sat_state.pose.theta - math.pi / 2)))) - 15 * satellite_state.twist.v_x
            control_message.thrust.f_y = -30 * (satellite_state.pose.y - ((dead_sat_state.pose.y)+(0.25*sin(dead_sat_state.pose.theta - math.pi / 2)))) - 10 * satellite_state.twist.v_y
            control_message.thrust.tau = -30 * (satellite_state.pose.theta - ((dead_sat_state.pose.theta)+math.pi)) - 18.0 * satellite_state.twist.omega
        elif sqrt(xdistance**2+ydistance**2)<(radius): #shpere# Set thrust command values, basic PD controller that drives the sat to [0, -1]
            control_message.thrust.f_x = -2 * (satellite_state.pose.x - ((dead_sat_state.pose.x)+(0.25*cos(dead_sat_state.pose.theta - math.pi / 2)))) - 2 * satellite_state.twist.v_x
            control_message.thrust.f_y = -2 * (satellite_state.pose.y - ((dead_sat_state.pose.y)+(0.25*sin(dead_sat_state.pose.theta - math.pi / 2)))) - 1 * satellite_state.twist.v_y
            if sqrt(xdistance**2+ydistance**2)<0.4:
                control_message.thrust.tau = -10 * (satellite_state.pose.theta - ((dead_sat_state.pose.theta)+math.pi)) - 30.0 * satellite_state.twist.omega    
            else:    
                control_message.thrust.tau = -30 * (satellite_state.pose.theta - ((dead_sat_state.pose.theta)+math.pi)) - 20.0 * satellite_state.twist.omega                   
       
       
        else:  #FUERA ESFERA
            if ydistance<(radius*4*diversion) and xdistance>radius:
                #and abs(math.pi+satellite_state.pose.theta - ((dead_sat_state.pose.theta)+math.pi))<(math.pi/2):
                #and abs(math.pi+satellite_state.pose.theta - ((dead_sat_state.pose.theta)+math.pi))>(math.pi/2):
                print("LOOP1")
                control_message.thrust.f_y = -2 * (3*radius+satellite_state.pose.y - ((dead_sat_state.pose.y)+(0.44*sin(dead_sat_state.pose.theta - math.pi / 2)))) - 5 * satellite_state.twist.v_y
                control_message.thrust.f_x = -2 * (satellite_state.pose.x - ((dead_sat_state.pose.x)+(0.44*cos(dead_sat_state.pose.theta - math.pi / 2)))) - 5 * satellite_state.twist.v_x
                if sqrt(xdistance**2+ydistance**2)<0.75:
                    control_message.thrust.tau = -30 * (satellite_state.pose.theta - ((dead_sat_state.pose.theta)+math.pi)) - 25.0 * satellite_state.twist.omega    
            
            elif xdistance<(radius*4*-diversion) and ydistance>radius:
             #   #and abs(math.pi+satellite_state.pose.theta - ((dead_sat_state.pose.theta)+math.pi))<(math.pi/2):
                print("LOOP2")
                control_message.thrust.f_x = -2 * (3*radius+satellite_state.pose.x - ((dead_sat_state.pose.x)+(0.44*cos(dead_sat_state.pose.theta - math.pi / 2)))) - 5 * satellite_state.twist.v_x
                control_message.thrust.f_y = -2 * (satellite_state.pose.y - ((dead_sat_state.pose.y)+(0.44*sin(dead_sat_state.pose.theta - math.pi / 2)))) - 5 * satellite_state.twist.v_y
                if sqrt(xdistance**2+ydistance**2)<0.75:
                   control_message.thrust.tau = -30 * (satellite_state.pose.theta - ((dead_sat_state.pose.theta)+math.pi)) - 25.0 * satellite_state.twist.omega    
            
            else:
                control_message.thrust.f_x = -2 * (satellite_state.pose.x - ((dead_sat_state.pose.x)+(0.44*cos(dead_sat_state.pose.theta - math.pi / 2)))) - 5 * satellite_state.twist.v_x
                control_message.thrust.f_y = -2 * (satellite_state.pose.y - ((dead_sat_state.pose.y)+(0.44*sin(dead_sat_state.pose.theta - math.pi / 2)))) - 5 * satellite_state.twist.v_y
                if sqrt(xdistance**2+ydistance**2)<0.75:
                    control_message.thrust.tau = -50 * (satellite_state.pose.theta - ((dead_sat_state.pose.theta)+math.pi)) - 25.0 * satellite_state.twist.omega    
            


        print("xdist", (xdistance))
        print("ydist", (ydistance))
        #```pipenv run python ./software/simulator/sim_gui.py --challenge 4```
>>>>>>> Stashed changes
        # Return control message
        return control_message

    def team_reset(self) -> None:
        # Run any reset code
        pass