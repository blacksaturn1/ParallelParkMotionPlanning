import pygame
import math
from math import pi
from  ackermann import RobotAckermann
from environment import Envir




pygame.init()
start=(200,200)
dims=(800,800)
running=True

robot=RobotAckermann(start,
            r"diff_drive.png",
            .1*3779.52)
env=Envir(dims,robot)

dt=0
lastime=pygame.time.get_ticks()
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        robot.move(event)
    dt = (pygame.time.get_ticks()-lastime)/1000
    lastime=pygame.time.get_ticks()
    pygame.display.update()
    env.map.fill(env.black)
    env.draw_obstacles()
    robot.move()
    robot.draw(env.map)

    env.write_info()
  