import machine
from machine import Pin

import math

import micropython
micropython.alloc_emergency_exception_buf(100)

class Encoder():
    def __init__(self, pinA, pinB, rev = False):
        self.pinA = Pin(pinA, Pin.IN, Pin.PULL_DOWN)
        self.pinB = Pin(pinB, Pin.IN, Pin.PULL_DOWN)
        self.rev = rev
        
        self.value = 0
        self.prev_value = 0
        
        self.pinA.irq(trigger= Pin.IRQ_RISING, handler=self.callback)
        
    def callback(self, p):
        if(self.pinB.value() == 1):
            self.value += 1
        else:
            self.value -= 1
    
    
    def getRot(self):
        return (self.value / 134.4) * 2 * math.pi
    
    # Calculates velocity in rads/s
    def getVelRot(self, dt):
        vel = ((self.value - self.prev_value) / (dt * 134.4)) * math.pi
        self.prev_value = self.value
        return vel

class Motor:
    def __init__(self, pin_A, pin_B, has_dir = False):
        self.pin_A = Pin(pin_A, machine.Pin.OUT)
        self.pin_B = Pin(pin_B, machine.Pin.OUT)
        self.pin_A_pwm = machine.PWM(self.pin_A)
        self.pin_B_pwm = machine.PWM(self.pin_B)
        
        self.pin_A_pwm.freq(1 * 1000)
        self.pin_B_pwm.freq(1 * 1000)
        
        self.has_dir = has_dir
    
    def setEncoder(self, pin_A_num, pin_B_num):
        self.encoder = Encoder(pin_A_num, pin_B_num)
    
    def setPower(self, power):
        
        if(self.has_dir):
            if(power > 0):
                self.dir_pin.on()
            else:
                self.dir_pin.off()
            
            power = abs(power)

            self.pwm.duty_u16(int(power * 62536.0))
            
        else:
            # print(power)
            if(power > 0):
                # self.pin
                self.pin_A_pwm.duty_u16(int(abs((power)) * 63536))
                self.pin_B_pwm.duty_u16(0)
            else:
                self.pin_B_pwm.duty_u16(int(abs(power) * 63536))
                self.pin_A_pwm.duty_u16(0)
                

class Motors:
    def __init__(self):
        self.motor1 = Motor(4, 3)
        self.motor1.setEncoder(22, 21)
        
        self.motor2 = Motor(6, 5)
        self.motor2.setEncoder(20, 19)
        
        self.motor3 = Motor(8, 7)
        self.motor3.setEncoder(18, 17)
       


