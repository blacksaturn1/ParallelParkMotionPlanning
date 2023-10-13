import pygame
from robot import Robot
import math

class RobotDiff(Robot):
    def __init__(self,startpos, robotImg,width) -> None:
        self.m2p=3779.52
        # self.m2p=0.1
        self.w=width
        self.x=startpos[0]
        self.y=startpos[1]
        self.theta=0
        self.vl=0.00 * self.m2p
        self.vr=0.00 * self.m2p
        self.maxspeed=0.02 * self.m2p
        self.minspeed=0.01 * self.m2p
        self.img = pygame.image.load(robotImg)
        self.rotated = self.img
        self.rect=self.rotated.get_rect(center=(self.x,
                                                self.y))
        self.dt = 0.005
    def draw(self,map:pygame.Surface):
        map.blit(self.rotated,self.rect)
    
    def move(self,event=None):
        if event is not None:
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_KP4:
                    self.vl+=0.001*self.m2p
                elif event.key == pygame.K_KP1:
                    self.vl-=0.001*self.m2p
                elif event.key == pygame.K_KP6:
                    self.vr+=0.001*self.m2p
                elif event.key == pygame.K_KP3:
                    self.vr-=0.001*self.m2p
                elif event.key == pygame.K_KP8:
                    self.vr+=0.001*self.m2p
                    self.vl+=0.001*self.m2p
                elif event.key == pygame.K_KP5:
                    self.vr=0
                    self.vl=0
        self.x+=(self.vl + self.vr)/2*math.cos(self.theta)*self.dt
        # y is opposite direction of screen
        self.y-=(self.vl + self.vr)/2*math.sin(self.theta)*self.dt
        self.theta += (self.vr-self.vl)/self.w*self.dt
        #self.rotated=self.img
        self.rotated=pygame.transform.rotozoom(self.img,
                                               math.degrees(self.theta),1)
        self.rect = self.rotated.get_rect(center=(self.x,self.y))
    
    def get_write_info(self):
        txt = f"Vl = {self.vl} Vr = {self.vr} THETA={self.theta}"
        return txt