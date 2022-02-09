# Writing your first controller
You will interact with the sattalite by implementing a set of funtions within the team controller file. A frame work is already written with inputs and outputs. Your challange is to write out a controller that brings the live satalite in line with the dead satalite and docks them.

For in-person particepents, you will only worry about the "level 1" challange, which contains a stationay dead satalite.

## Interfaces
We use [Google Protbuf](https://developers.google.com/protocol-buffers) to send information between the controller and satalte (both physical and simulated) these provide a standard set of type enforced interfaces and make it easier not to mess data up. The interfaces you will be dealing with are listed below

### Satalilte state: 
```
message SatalliteState {

    // Satellite location
    Pose2D pose

    // Satellite velocity
    Twist2D twist

    // Used fuel (tracks impulse over time)
    float fuel
}
```

### Pose, Twist and Wrench: 
These are just higher dimensoinal versions of position, velocity and force.
```
message Pose2D {
    float x = 1; // in meters
    float y = 2; // in meters
    float theta = 3; // in rads
}

// 2D Twist, translatonal + rotational velocity
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