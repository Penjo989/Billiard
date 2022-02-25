import pygame
import math
from functions import *
from interface import text
import random
#colors
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
BROWN = (165,42,42)
PINK = (255,105,180)
BLACK = (0,0,0)
WHITE = (255,255,255)
PURPLE = (128,0,128)
ORANGE = (255,165,0)
BURGUNDY = (128, 0, 32)
WOOD = (202,164,114)
DARK_WOOD = (68, 48, 34)
DARK_GREEN = (0, 100, 0)

#CONSTANTS
BALL_AMOUNT = 15
BALL_COLORS = [YELLOW, BLUE, RED, PURPLE, ORANGE, GREEN, BURGUNDY, BLACK, YELLOW, BLUE, RED, PURPLE, ORANGE, GREEN, BURGUNDY]
CUE_LEN = 200
CUE_MAX_DIST = 200
CUE_MIN_DIST = 50
CUE_WIDTH = 5
BALL_RAD = 15
MINIMUM_BALL_VEL = 2
BORDER_WIDTH = 10
BORDER_HEIGT = 10
HOLE_RADIUS = 50

class Board:
    def __init__(self, surface, size, color = RED):
        self.color = color
        self.surface = surface
        self.size = size
        self.ball_movement = False
        self.turn = "open"
        self.cue_cords = "free"
        self.balls = []
        self.holes = []
        self.friction = 100
        self.power_var = 1.5
        self.show_holes = False
        self.start_pos_height = self.size[1]*0.8
        self.ball_start_pos = []
        self.generate_start_pos()
        for i in range(1, BALL_AMOUNT+1):
            if (i<9):
                self.balls.append(ball(BALL_COLORS[i-1], i, "closed", self.ball_start_pos[i-1], self.surface))
            else:
                self.balls.append(ball(BALL_COLORS[i-1], i, "open", self.ball_start_pos[i-1], self.surface))
        self.holes.append(hole([0,0], self.surface, HOLE_RADIUS))
        self.holes.append(hole([self.size[0],0], self.surface, HOLE_RADIUS))
        self.holes.append(hole(self.size, self.surface, HOLE_RADIUS))
        self.holes.append(hole([0,self.size[1]], self.surface, HOLE_RADIUS))
        self.holes.append(hole([0,self.size[1]/2], self.surface, HOLE_RADIUS*0.8))
        self.holes.append(hole([self.size[0], self.size[1]/2], self.surface, HOLE_RADIUS*0.8))

        self.balls.append(ball(WHITE, 0, "closed", [self.size[0]/2, self.size[1]*0.2], self.surface, 1.73))



    def update(self, interval):
        self.update_balls(interval)

    def update_balls(self, interval):
        self.ball_movement = False
        for ball in self.balls:
            if(ball.vel[0] != 0 or ball.vel[1] != 0):
                self.ball_movement = True
        for ball in self.balls:
            if ball.on_board:
                for other_ball in self.balls[self.balls.index(ball):]:
                    if other_ball != ball and other_ball.on_board == True:
                        vel1 = self.get_vel(interval, ball)
                        pos1 = [ball.pos[0] + vel1[0]*interval, ball.pos[1] + vel1[1]*interval]
                        vel2 = self.get_vel(interval, other_ball)
                        pos2 = [other_ball.pos[0] + vel2[0]*interval, other_ball.pos[1] + vel2[1]*interval]
                        if(get_dist(pos2, pos1) < ball.radius + other_ball.radius):
                            ball.vel, other_ball.vel = handle_crash(ball, other_ball)

                ball.vel = self.get_vel(interval, ball)
                ball.pos[0] += ball.vel[0]*interval
                ball.pos[1] += ball.vel[1]*interval
                for hole in self.holes:
                    hole.check_if_in(ball)

    def display(self, cue_state, mouse_pos = (0,0)):
        self.surface.fill(self.color)
        for hole in self.holes:
            hole.display()
        pygame.draw.rect(self.surface, DARK_WOOD, (0, 0, BORDER_WIDTH, self.size[1]))
        pygame.draw.rect(self.surface, DARK_WOOD, (self.size[0] - BORDER_WIDTH, 0, BORDER_WIDTH, self.size[1]))
        pygame.draw.rect(self.surface, DARK_WOOD, (0, self.size[1]-BORDER_HEIGT, self.size[0], BORDER_HEIGT))
        pygame.draw.rect(self.surface, DARK_WOOD, (0, 0, self.size[0], BORDER_HEIGT))

        if self.show_holes:
            for hole in self.holes:
                hole.display()
        for ball in self.balls:
            ball.display()

        if not self.ball_movement:
            if cue_state == "free":
                if(self.cue_cords != "free"):
                    distance = mouse_pos[1] - self.cue_cords[1]
                    if distance >= CUE_MIN_DIST:
                        self.ball_movement = True
                        self.balls[15].vel = [(self.balls[15].pos[0] - self.get_cue_pos(mouse_pos, distance)[0])*self.power_var, (self.balls[15].pos[1] - self.get_cue_pos(mouse_pos, distance)[1])*self.power_var]
                self.cue_cords = "free"
                pygame.draw.line(self.surface, WOOD, self.balls[15].pos, self.get_cue_pos(mouse_pos, CUE_LEN), CUE_WIDTH)
            elif cue_state == "pushed":
                if self.cue_cords == "free":
                    self.cue_cords = (mouse_pos)
                distance = mouse_pos[1] - self.cue_cords[1]
                if distance> CUE_MAX_DIST:
                    distance = CUE_MAX_DIST
                if distance>0:
                    pygame.draw.line(self.surface, WOOD, self.get_cue_pos(mouse_pos, distance), self.get_cue_pos(mouse_pos, CUE_LEN + distance), CUE_WIDTH)
                else:
                    pygame.draw.line(self.surface, WOOD, self.balls[15].pos, self.get_cue_pos(mouse_pos, CUE_LEN), CUE_WIDTH)
    def get_cue_pos(self, mouse_pos, distance):
        if self.cue_cords != "free":
            mouse_pos = self.cue_cords
        incline = get_m(mouse_pos, self.balls[15].pos)
        alpha = math.atan(incline)
        #print(f"m: {m}, alpha: {alpha}, cos(alpha): {math.cos(alpha)}")
        if(self.balls[15].pos[0]> mouse_pos[0]):
            x = -1
        else:
            x = 1
        return (self.balls[15].pos[0] + math.cos(alpha)*distance*x, self.balls[15].pos[1] + math.sin(alpha) * distance * x)
    def get_vel(self, interval, ball):
        vel = calc_speed(ball, self.friction, interval)
        if abs(math.sqrt(vel[0]*vel[0] + vel[1]*vel[1])) < MINIMUM_BALL_VEL:
            vel = [0, 0]
        if ball.pos[0] + vel[0]*interval - ball.radius < BORDER_WIDTH or ball.pos[0] + vel[0]*interval  + ball.radius > self.size[0] - BORDER_WIDTH:
            vel[0] *= -1
        if ball.pos[1] + vel[1]*interval - ball.radius< BORDER_HEIGT or ball.pos[1] + vel[1]*interval + ball.radius> self.size[1] - BORDER_HEIGT:
            vel[1] *=-1
        return vel
    def generate_start_pos(self):
        rad = 1.2*BALL_RAD
        for i in range(0,5):
            self.ball_start_pos.append([(self.size[0] - rad*2*5)/2 + 2*rad*(i+0.5), self.start_pos_height-rad])
        for i in range(0,4):
            self.ball_start_pos.append([(self.size[0] - rad*2*4)/2 + 2*rad*(i+0.5), self.start_pos_height-rad*3])
        for i in range(0,3):
            self.ball_start_pos.append([(self.size[0] - rad*2*3)/2 + 2*rad*(i+0.5), self.start_pos_height-rad*5])
        for i in range(0,2):
            self.ball_start_pos.append([(self.size[0] - rad*2*2)/2 + 2*rad*(i+0.5), self.start_pos_height-rad*7])
        self.ball_start_pos.append([(self.size[0] - rad*2)/2 + rad, self.start_pos_height-rad*9])


class ball:
    def __init__(self, color, number, type, pos, surface, mass = 1):
        self.color = color
        self.number = number
        self.type = type
        self.surface = surface
        self.pos = pos
        self.on_board = True
        self.vel = [0,0]
        self.radius = BALL_RAD
        self.mass = mass
        self.text = text(str(self.number), BLACK, self.pos[0], self.pos[1], 37, self.surface)


    def display(self):
        if self.type == "open":
            pygame.draw.circle(self.surface, WHITE, self.pos, self.radius)
            pygame.draw.circle(self.surface, self.color, self.pos, self.radius*0.95)
        else:
            pygame.draw.circle(self.surface, self.color, self.pos, self.radius)
        pygame.draw.circle(self.surface, WHITE, self.pos, self.radius/1.5)

        #if self.number != 0:
            #self.text.display()
class hole:
    def __init__(self, pos, surface, radius):
        self.pos = pos
        self.balls = []
        self.radius = radius
        self.surface = surface
    def display(self):
        pygame.draw.circle(self.surface, DARK_GREEN, self.pos, self.radius)
    def check_if_in(self, ball):
        if get_dist(self.pos, ball.pos) < self.radius:
            self.balls.append(ball.number)
            ball.vel = [0,0]
            ball.pos = [-100, -100]
