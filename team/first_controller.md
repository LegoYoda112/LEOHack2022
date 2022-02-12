# Writing your first controller
You will interact with the satellite by implementing a set of functions within the team controller file. A frame work is already written with inputs and outputs. Your challenge is to write out a controller that brings the live satellite in line with the dead satellite and docks them, we will define what "dock" means later.

For in-person participants, you will only worry about the "level 1" challenge, which contains a stationary dead satellite. Note that this 

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

    // Satellite location
    Pose2D pose

    // Satellite velocity
    Twist2D twist

    // Used fuel (tracks impulse over time)
    float fuel
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