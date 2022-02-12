# Writing your first controller
You will interact with the satellite by implementing a set of functions within the team controller file. Your challenge is to write a controller that brings the live satellite in line with the dead satellite and docks them, we will define what "dock" means later.

For in-person participants, you will only worry about the "level 1" challenge, which contains a stationary dead satellite.

## Interfaces
We use [Google Protbuf](https://developers.google.com/protocol-buffers) to send information between the controller and satellite (both physical and simulated) these provide a standard set of type enforced interfaces and make it easier not to mess data up. The interfaces you will be dealing with are listed below

### Satellite state: 
Contains the position and velocity of a satellite 
``` protobuf
message SatelliteState {

    // Satellite location
    Pose2D pose

    // Satellite velocity
    Twist2D twist

    // Used fuel (tracks impulse over time)
    float fuel
}
```

### Pose, Twist and Wrench: 
These are just higher dimensional versions of position, velocity and force. All are given in "world coordinates". 
``` protobuf
message Pose2D {
    float x = 1; // in meters
    float y = 2; // in meters
    float theta = 3; // in rads
}

// 2D Twist, translational + rotational velocity
message Twist2D {
    float v_x = 1; // in m/s
    float v_y = 2; // in m/s
    float omega = 3; // in rad/s
}

// 2D Wrench, force + torque
message Wrench2D {
    float f_x = 1; // in N
    float f_y = 2; // in N
    float tau = 3; // in Nm
}
```

### Control message: 
``` protobuf
message ControlMessage {
    // Wether or not to apply sent thrust commands
    bool active = 1;

    // Thrust command
    Wrench2D thrust = 2;

    // Absolute pose read by the camera system
    Pose2D absolute_pose = 3;
    
    // Servo states (for physical robot)
    ServoStates servo_states = 4;
}
```

For instance, to get the x position of the dead sat we can use: `dead_sat_state.pose.x`.

## Moving to a position
An example of a very simple controller that moves the sat to [1,1] using a simple [PD controller](https://en.wikipedia.org/wiki/PID_controller).

``` python
control_message = sat_msgs.ControlMessage()

control_message.thrust.f_x = -2.0 * (satellite_state.pose.x - 1) - 3.0 * satellite_state.twist.v_x
control_message.thrust.f_y = -2.0 * (satellite_state.pose.y - 1) - 3.0 * satellite_state.twist.v_y

return control_message
```

The x force is set to be the inverse of the error between pose.x and 1, this "pulls" the sat towards 1, in the same way a spring does. In addition, an extra term is present that adds force inversely proportional to the speed, actively damping the movement (the faster it goes, the more this force will push back). The next line does the same, but for y force.
