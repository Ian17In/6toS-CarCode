import machine as m
import time as t

# Configuracion del GPIO

f = 100
duty = 512

"""
    Motor A:
    A1M1: Pin 16
    A2M1: Pin 17

    Motor B:
    B1M2: Pin 18
    B2M2: Pin 19

"""

A1M1 = m.PWM(m.Pin(16), freq=f, duty=duty)
A2M1 = m.PWM(m.Pin(17), freq=f, duty=0)

B1M2 = m.PWM(m.Pin(18), freq=f, duty=duty)
B2M2 = m.PWM(m.Pin(19), freq=f, duty=0)

# Funciones para controlar las direcciones y velocidades

def forward():
    A1M1.duty(duty)
    A2M1.duty(0)

    B1M2.duty(duty)
    B2M2.duty(0)

def backward():
    A1M1.duty(0)
    A2M1.duty(duty)

    B1M2.duty(0)
    B2M2.duty(duty)

def left():
    A1M1.duty(0)
    A2M1.duty(duty)

    B1M2.duty(duty)
    B2M2.duty(0)

def right():
    A1M1.duty(duty)
    A2M1.duty(0)
    
    B1M2.duty(0)
    B2M2.duty(duty)

t.sleep(1)
forward()
t.sleep(2)
backward()