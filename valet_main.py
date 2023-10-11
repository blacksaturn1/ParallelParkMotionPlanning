import pygame
import math
from math import pi

class Envir:
    def __init__(self,dimensions):
        #colors
        self.black=(0,0,0)
        self.white=(255,255,255)
        self.green=(0,255,0)
        self.blue=(0,0,255)
        self.red=(255,0,0)
        self.yel=(255,255,0)
        # map dim
        self.height = dimensions[0]
        self.width = dimensions[1]
        # window settings
        pygame.display.set_caption("Robot")
        self.map=pygame.display.set_mode((self.width,self.height))
        self.font=pygame.font.Font('freesansbold.ttf',25)
        self.text = self.font.render('default',True,self.white,self.black)
        self.textRect = self.text.get_rect()
        self.textRect.center=(dimensions[1]-600,dimensions[0]-100)

    def write_info(self,v,psi,theta):
        txt = f"V = {v} PSI={psi} THETA={theta}"
        self.text=self.font.render(txt,True,self.white,self.black)
        self.map.blit(self.text,self.textRect)

class RobotAckerman():
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
        
        self.rect=self.rotated.get_rect(center=(self.x,
                                                self.y))
    def draw(self,map:pygame.Surface):
        map.blit(self.rotated,self.rect)
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
        self.x+=self.v*math.cos(self.theta)*dt
        # y is opposite direction of screen
        self.y-=self.v*math.sin(self.theta)*dt
        
        thetadelta=((self.v/self.l)*math.tan(math.radians(self.psi)))*dt #%(360)
        # if self.psi != 0:
            
        # else:
        #     thetadelta=0
        #thetadelta = thetadelta % (2*pi)
        if thetadelta > pi:
                thetadelta = (2*pi) - thetadelta
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



class RobotDiff():
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
        self.minspeed=0.02 * self.m2p
        self.img = pygame.image.load(robotImg)
        self.rotated = self.img
        self.rect=self.rotated.get_rect(center=(self.x,
                                                self.y))
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
        self.x+=(self.vl + self.vr)/2*math.cos(self.theta)*dt
        # y is opposite direction of screen
        self.y-=(self.vl + self.vr)/2*math.sin(self.theta)*dt
        self.theta += (self.vr-self.vl)/self.w*dt
        #self.rotated=self.img
        self.rotated=pygame.transform.rotozoom(self.img,
                                               math.degrees(self.theta),1)
        self.rect = self.rotated.get_rect(center=(self.x,self.y))
    


pygame.init()
start=(200,200)
dims=(800,800)
running=True
env=Envir(dims)

robot=RobotAckerman(start,
            r"diff_drive.png",
            .1*3779.52)
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
    robot.move()
    robot.draw(env.map)

    env.write_info(int(robot.v),
                   int(robot.psi),
                   int(robot.theta))
    # env.write_info(int(robot.vl),
    #                 int(robot.vr),
    #                 int(robot.theta))