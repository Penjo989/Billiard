import pygame
import socket
import math

def get_m(pos2, pos1):
    if (pos2[0]-pos1[0]) == 0:
        pos2 = (pos2[0]+0.1, pos2[1])
    return (pos2[1]-pos1[1])/(pos2[0]-pos1[0])

def get_dist(pos1, pos2):
    return math.sqrt((pos2[0]-pos1[0])*(pos2[0]-pos1[0]) + (pos2[1]-pos1[1])*(pos2[1]-pos1[1]))

def get_angle_between_vectors(v1, v2):
    angle1 = get_angle_of_vector(v1)
    angle2 = get_angle_of_vector(v2)
    if angle1 > angle2:
        return angle1 - angle2
    return angle2 - angle1

def get_angle_of_vector(v1):
        if v1[0] != 0:
            if v1[0]>0:
                if v1[1] > 0:
                    angle = math.degrees(math.atan(v1[1]/v1[0]))
                else:
                    angle = 360 + math.degrees(math.atan(v1[1]/v1[0]))
            else:
                if v1[1] > 0:
                    angle = 180 - math.degrees(math.atan(v1[1]/-v1[0]))
                else:
                    angle = 180 + math.degrees(math.atan(v1[1]/v1[0]))
        else:
            if v1[1] > 0:
                angle = 90
            else:
                angle = 270
        return angle

def calc_crash(m1, m2, v1, v2):
    u1 = (m1*v1 - m2*v1 + 2*m2*v2)/(m1 + m2)
    u2 = v1 + u1 - v2

    return u1, u2

    #return [ball1.vel[0] + u1*math.cos(math.radians(omega)), ball1.vel[1] + u1*math.sin(math.radians(omega))], [ball2.vel[0] + u2*math.cos(math.radians(omega)), ball2.vel[1] + u2*math.sin(math.radians(omega))]

def calc_speed(ball, friction, interval):
    v = math.sqrt(ball.vel[0]*ball.vel[0] + ball.vel[1]*ball.vel[1]) - friction*interval
    if(ball.vel[0] > 0):
        x = 1
    else:
        x = -1
    if(ball.vel[1] > 0):
        y = 1
    else:
        y = -1
    if(ball.vel[0] != 0):
        alpha = math.atan(abs(ball.vel[1])/abs(ball.vel[0]))
    else:
        if v>0:
            return [0, v*y]
        return [0,0]
    return [v*math.cos(alpha)*x, v*math.sin(alpha)*y]



def get_angle_of_crash(ball1, ball2):
    m = get_m(ball1.pos, ball2.pos)
    alpha = math.atan(m)
    return alpha

def transform_vect(vector, angle):
    new_vect_x = math.cos(angle)*vector[0] + math.sin(angle)* vector[1]
    new_vect_y = math.cos(angle)* vector[1] - math.sin(angle)*vector[0] 
    return [new_vect_x, new_vect_y]

def handle_crash(ball1, ball2):
    angle = get_angle_of_crash(ball1, ball2)
    v1 = transform_vect(ball1.vel, angle)
    v2 = transform_vect(ball2.vel, angle)
    v1[0], v2[0] = calc_crash(ball1.mass, ball2.mass, v1[0], v2[0])
    v1 = transform_vect(v1, -angle)
    v2 = transform_vect(v2, -angle)
    return v1, v2
