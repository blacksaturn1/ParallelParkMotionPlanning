from typing import List, Optional, Tuple
import pygame
import math
from valet.states.state import State

class AckermannState(State):

    def __init__(
        self,
        xy: Tuple[float, float],
        theta: float,
        psi: float,
        v: float,
        img
    ):
        super().__init__(xy,theta,img)
        self.psi = round(psi,1)
        self.v=v
        # self.img = img
        self.rotated = pygame.transform.rotozoom(self.img,math.degrees(self.theta),1)
        self.rect = self.rotated.get_rect(center=(self.x,self.y))
        self.rect.width*=1.3
        self.rect.height*=1.3
        self.cost_to_come=0
        self.cost_to_go = 0
    
    # def get_cost(self,goal):
    #     x,y,theta = goal
    #     euclideanCost = ((x- self.x)**2 + (y- self.y)**2)**.5
    #     thetaCost = abs(theta-self.theta)
    #     return euclideanCost
        #return .5*euclideanCost + .5*thetaCost
        

    # def get_location(self):
    #     return (self.x,self.y,self.theta)
    
    # def __hash__(self):
    #     return hash((self.x, self.y,self.theta))
    
    # def __eq__(self, other):
    #     return (self.x, self.y,self.theta,self.psi,self.v) == (other.x, other.y,other.theta,other.psi,other.v)
    
    # def __lt__(self, other):
    #     return (self.cost_to_come+self.cost_to_go)  < (other.cost_to_come+other.cost_to_go)
            