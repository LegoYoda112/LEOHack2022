from motors import Motors

from math import sqrt, sin, cos

robot_radius = 67.4 / 100.0 # m
wheel_dia = 80.0 / 1000.0 # m

J3 = -wheel_dia / robot_radius

x_scale = 1.42
y_scale = x_scale

J = [[-0.03 * x_scale, 0.015 * x_scale, 0.015 * x_scale],
     [0.0, 0.0259808 * y_scale, -0.0259808 * y_scale],
     [J3, J3, J3]]

invJ = [[-22.2222, 0.0, 1.94444],
        [11.1111, -19.245, 1.94444],
        [11.1111, 19.245, 1.94444]]

class Kinematics():
    def __init__(self):
        self.x = 0
        self.vel_x = 0
        self.y = 0
        self.vel_y = 0
        self.theta = 0
        self.omega = 0
        self.m = Motors()


    def twistVel(self, x, y, omega):
        x = x # m/s
        y = y # m/s
        
        # print("here")
        
        Kx = 0.02 # X velocity constnat
        Kxff = 0.3
        
        Ky = 0.02 # Y velocity constant
        Kyff = 0.3
        
        Ko = 0.05 # Z
        Koff = 0.3
        
        # Run simple proportinal controller
        x_pow = Kx * (x - self.vel_x) + x * Kxff
        y_pow = Ky * (y - self.vel_y) + y * Kyff
        theta_pow = Ko * (omega - self.omega) + omega * Koff
        
        # print(self.omega)
        
        #x_pow = x
        #y_pow = y
        #theta_pow = omega
        
        motor1 = x_pow * invJ[0][0] + y_pow * invJ[0][1] + theta_pow * invJ[0][2]
        motor2 = x_pow * invJ[1][0] + y_pow * invJ[1][1] + theta_pow * invJ[1][2]
        motor3 = x_pow * invJ[2][0] + y_pow * invJ[2][1] + theta_pow * invJ[2][2]
        
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
        
        self.vel_x = q_1 * J[0][0] + q_2 * J[0][1] + q_3 * J[0][2]
        self.vel_y = -(q_1 * J[1][0] + q_2 * J[1][1] + q_3 * J[1][2])
        self.omega = q_1 * J[2][0] + q_2 * J[2][1] + q_3 * J[2][2]
        
        dx = self.vel_x * dt
        dy = self.vel_y * dt
        
        self.x += dx * cos(self.theta) - dy * sin(self.theta) 
        self.y += dx * sin(self.theta) + dy * cos(self.theta)
        self.theta += self.omega * dt



