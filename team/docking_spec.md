# Docking Spec
To dock a live satellite to a dead one, we must make a rough approach to get to the outside of the keepout sphere and then enter the sphere adhering to a set of restrictions.


## Rough Approach
In a real orbit, a long distance approach procedure would be highly complex, consisting of raising the vehicles orbit, aligning velocity etc. In our 2D system, this is much simpler, as we do not have to deal with orbital mechanics.

| Item | value      |
| ----- | ----- |
| Max velocity | 1 m/s    |

## Final approach
With in orbit objects such as the ISS, a keepout sphere is defined for safety, any vehicle entering this sphere must adhere to velocity, proximity and other limits. Once the vehicle has approached the edge of the keepout sphere, it can transition into a slower, final approach. This has a more restrictive set of requirements.

| Item | value      |
| ----- | ----- |
| Sphere radius | 0.5 m         |
| Max velocity in sphere |  0.2m/s |

## Docking
Once we are within a specified distance to the sat, we will considered it docked. Specifications are listed below.

| Item | tolerance      |
| ----- | ----- |
|x-offset | +-0.05 m         |
|y-offset | 0.25m +- 0.02 m   |
|theta-offset | +-0.1 rads (~6 degrees)  |
|max velocity | 0.05 m/s     |
|max angular velocity | 0.1 rads/s |

The simulator will print out messages telling you which of the specs you have achieved.