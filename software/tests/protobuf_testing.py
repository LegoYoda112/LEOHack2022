import sys
sys.path.append("../msgs/")
sys.path.append("software/msgs/")

import sat_descrip_pb2

test = sat_descrip_pb2.SataliteState()
test.teamID = 2346
test.active = True

# satPose = sat_descrip_pb2.Pose2D()
# satPose.x = 1.0
# satPose.y = 2.0
# satPose.theta = 3.0

test.pose.x = 1.0
test.pose.y = 2.0
test.pose.theta = 3.0

print(type(sat_descrip_pb2.SataliteState()))

serialized = test.SerializeToString()
