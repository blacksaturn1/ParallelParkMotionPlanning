import pygame
from robot import Robot

class Envir:
    def __init__(self,dimensions,robot:Robot):
        #colors
        self.robot=robot
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

    def write_info(self):
        txt = self.robot.get_write_info()
        self.text=self.font.render(txt,True,self.white,self.black)
        self.map.blit(self.text,self.textRect)

