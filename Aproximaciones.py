#import machine as m
import time as t
import math 

def RKX_aprox(x_0,r,theta,dotphiL,dotphiR,h):
    """
    Aproximación de la función f(x)
    """
    k1 = (r/2)*dotphiL*math.sin(theta) + (r/2)*dotphiR*math.cos(theta)
    k2 = (r/2)*dotphiL*math.sin(theta) + (r/2)*dotphiR*math.cos(theta) + (1/2)*k1*h
    k3 = (r/2)*dotphiL*math.sin(theta) + (r/2)*dotphiR*math.cos(theta) + (1/2)*h*k2
    k4 = (r/2)*dotphiL*math.sin(theta) + (r/2)*dotphiR*math.cos(theta) + h*k3

    return x_0 + (h/6)*(k1 + 2*k2 + 2*k3 + k4)  

def RKY_aprox(y_0,r,theta,dotphiL,dotphiR,h):
    """
    Aproximación de la función f(x)
    """
    k1 = (r/2)*dotphiL*math.cos(theta) - (r/2)*dotphiR*math.sin(theta)
    k2 = (r/2)*dotphiL*math.cos(theta) - (r/2)*dotphiR*math.sin(theta) + (1/2)*k1*h
    k3 = (r/2)*dotphiL*math.cos(theta) - (r/2)*dotphiR*math.sin(theta) + (1/2)*h*k2
    k4 = (r/2)*dotphiL*math.cos(theta) - (r/2)*dotphiR*math.sin(theta) + h*k3

    return y_0 + (h/6)*(k1 + 2*k2 + 2*k3 + k4)

def RKtheta_aprox(theta_0,r,dotphiL,dotphiR,s,h):
    """
    Aproximación de la función f(x)
    """
    k1 = (-r/s)*dotphiL + (1/2)*s*dotphiR
    k2 = (-r/s)*dotphiL + (1/2)*s*dotphiR + (1/2)*h*k1
    k3 = (-r/s)*dotphiL + (1/2)*s*dotphiR + (1/2)*h*k2
    k4 = (-r/s)*dotphiL + (1/2)*s*dotphiR + h*k3

    return theta_0 + (h/6)*(k1 + 2*k2 + 2*k3 + k4)



if __name__ == '__main__':
    r = 1
    theta_0 = 0
    dotphiL = 0
    dotphiR = 0
    s = 1
    h = 0.1
    x_0 = 0
    y_0 = 0
    
    for i in range(10):
        dotphiL = 0 + i
        dotphiR = 0 + i

        x_0 = RKX_aprox(x_0,r,theta_0,dotphiL,dotphiR,h)
        y_0 = RKY_aprox(y_0,r,theta_0,dotphiL,dotphiR,h)
        theta_0 = RKtheta_aprox(theta_0,r,dotphiL,dotphiR,s,h)

        print(f'Iteración {i+1}: ({x_0:.2f}, {y_0:.2f}, {theta_0:.2f})')

        t.sleep(1)