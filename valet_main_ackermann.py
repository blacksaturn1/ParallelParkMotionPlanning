import pygame
import math
from math import pi
from ackermann import RobotAckermann
from environment import Envir
from lattice import Lattice



pygame.init()
start=(100,100,0)
#goal_orientation=0
goal=(600, 650,0)
dims=(800,800)
running=True

robot=RobotAckermann(start,
            r"diff_drive.png",
            .1*3779.52,goal)
env=Envir(dims,robot,goal)

dt=0
lastime=pygame.time.get_ticks()
lattice = Lattice(start,goal)

while running:

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        robot.move(event)
    dt = (pygame.time.get_ticks()-lastime)/1000
    lastime=pygame.time.get_ticks()
    pygame.display.update()
    
    robot.move()
    lattice.add_neighbors(robot.plan())
    lattice.plan()
    nextMove = lattice.step(env.obstacleGrid)
    robot.drive(nextMove)
    env.map.fill(env.black)
    env.draw_obstacles()
    env.draw_goal()

    robot.draw(env.map)
    env.write_info()
    