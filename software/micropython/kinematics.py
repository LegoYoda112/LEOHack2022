from motors import Motors

from math import sqrt, sin, cos

robot_radius = 67.4 / 100.0 # m
wheel_dia = 80.0 / 1000.0 # m

J3 = wheel_dia / robot_radius 

J = [[-0.03, 0.015, 0.015],
     [0.0, -0.0259808, 0.0259808],
     [J3, J3, J3]]

invJ = [[-22.2222, 0.0, 1.94444],
        [11.1111, -19.245, 1.94444],
        [11.1111, 19.245, 1.94444]]

class Kinematics():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.theta = 0
        self.m = Motors()


    def twistVel(self, x, y, theta):
        x = x/1000.0 # mm/s
        y = y/1000.0 # mm/s
        
        motor1 = x * invJ[0][0] + y * invJ[0][1] + theta * invJ[0][2]
        motor2 = x * invJ[1][0] + y * invJ[1][1] + theta * invJ[1][2]
        motor3 = x * invJ[2][0] + y * invJ[2][1] + theta * invJ[2][2]
        
        #print(motor1)
        #print(motor2)
        #print(motor3)
        
        self.m.motor1.setPower(motor1)
        self.m.motor2.setPower(motor2)
        self.m.motor3.setPower(motor3)
        
    def twistVelAbsolute(self, x, y, omega):
        abs_x = x * cos(self.theta) - y * sin(self.theta)
        abs_y = x * sin(self.theta) + y * cos(self.theta)
        
        self.twistVel(-abs_x, -abs_y, omega)

    def updateOdom(self, dt):
        q_1 = self.m.motor1.encoder.getVelRot(dt)
        q_2 = self.m.motor2.encoder.getVelRot(dt)
        q_3 = self.m.motor3.encoder.getVelRot(dt)
        
        vel_x = q_1 * J[0][0] + q_2 * J[0][1] + q_3 * J[0][2]
        vel_y = q_1 * J[1][0] + q_2 * J[1][1] + q_3 * J[1][2]
        omega = q_1 * J[2][0] + q_2 * J[2][1] + q_3 * J[2][2]
        
        dx = vel_x * dt
        dy = vel_y * dt
        
        self.x += dx * cos(self.theta) + dy * sin(self.theta) 
        self.y += dx * sin(self.theta) - dy * cos(self.theta)
        self.theta += omega * dt

