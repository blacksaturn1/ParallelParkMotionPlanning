import pygame
import math
from math import pi
from robot import Robot

class RobotAckermann(Robot):
    def __init__(self,startpos, robotImg,width) -> None:
        self.m2p=3779.52
        # self.m2p=0.1
        self.w=width
        self.x=startpos[0]
        self.y=startpos[1]
        self.theta=0
        self.v=0.00 * self.m2p
        self.psi = 0
        self.maxspeed=0.02 * self.m2p
        self.minspeed=0.01 * self.m2p
        self.img = pygame.image.load(robotImg)
        self.rotated = self.img
        self.l=2.8 * 40
        self.dt = 0.005
        
        self.rect=self.rotated.get_rect(center=(self.x,
                                                self.y))
    def draw(self,map:pygame.Surface):
        map.blit(self.rotated,self.rect)

    def get_write_info(self):
        txt = f"V = {int(self.v)} PSI={int(self.psi)} THETA={int(self.theta)}"
        return txt
    
    def move(self,event=None):
        if event is not None:
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_UP:
                    self.v+=0.001*self.m2p
                elif event.key == pygame.K_DOWN:
                    self.v-=0.001*self.m2p
                elif event.key == pygame.K_RIGHT:
                    self.psi-=10
                    if self.psi<=-50:
                        self.psi=-50

                elif event.key == pygame.K_LEFT:
                    
                    self.psi+=10
                    if self.psi>=50:
                        self.psi=50    
                elif event.key == pygame.K_KP5:
                    self.v=0                    
        self.x+=self.v*math.cos(self.theta)*self.dt
        # y is opposite direction of screen
        self.y-=self.v*math.sin(self.theta)*self.dt
        
        thetadelta=((self.v/self.l)*math.tan(math.radians(self.psi)))*self.dt #%(360)
        # if self.psi != 0:
            
        # else:
        #     thetadelta=0
        #thetadelta = thetadelta % (2*pi)
        if thetadelta > math.pi:
                thetadelta = (2*math.pi) - thetadelta
                thetadelta = -1 * thetadelta
        

        self.theta += thetadelta

        if self.theta>2*pi:
            self.theta-=2*pi
        if self.theta<(-2*pi):
            self.theta+=2*pi
            
        
            
        #self.rotated=self.img
        self.rotated=pygame.transform.rotozoom(self.img,
                                               math.degrees(self.theta),1)
        self.rect = self.rotated.get_rect(center=(self.x,self.y))
