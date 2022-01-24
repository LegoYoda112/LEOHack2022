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
    def __init__(self, dir_pin_num, pwm_pin_num):
        self.dir_pin = Pin(dir_pin_num, machine.Pin.OUT)
        self.pwm_pin = Pin(pwm_pin_num, machine.Pin.OUT)
        self.pwm = machine.PWM(self.pwm_pin)
        
        self.pwm.freq(100000)
    
    def setEncoder(self, pin_A_num, pin_B_num):
        self.encoder = Encoder(pin_A_num, pin_B_num)
    
    def setPower(self, power):
        if(power > 0):
            self.dir_pin.on()
        else:
            self.dir_pin.off()
        
        power = abs(power)
        self.pwm.duty_u16(int(power * 65536.0))
        

class Motors:
    def __init__(self):
        self.motor1 = Motor(4, 3)
        self.motor1.setEncoder(22, 21)
        
        self.motor2 = Motor(6, 5)
        self.motor2.setEncoder(20, 19)
        
        self.motor3 = Motor(8, 7)
        self.motor3.setEncoder(18, 17)
       
