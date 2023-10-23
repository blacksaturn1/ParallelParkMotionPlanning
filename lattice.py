from ackermannState import AckermannState
from typing import List, Optional, Tuple

class Lattice:

    def __init__(self,location:Tuple[float,float,float],goal:Tuple[float,float,float]) -> None:
        self.currentLocation=location
        self.goal=goal
        self.neigbors:list[AckermannState]=[]
        self.path: dict[AckermannState,AckermannState]={}
        self.cost: dict[AckermannState,float]={}


    def add_neighbors(self, neighbors):
        self.neigbors=neighbors

    def plan(self):
        for neighbor in self.neigbors:
            self.cost[neighbor]=self.calculateCost(neighbor)

    def isCollision(self,state,obstacleGrid):
        return False
    
    def step(self,obstacleGrid):
        lowestCost=9999
        lowestCostNeighbor=None
        for key,value in self.cost.items():
            if value<lowestCost:
                if not self.isCollision(key,obstacleGrid):
                    lowestCost=value
                    lowestCostNeighbor=key
        self.cost={}
        self.neigbors={}
        return lowestCostNeighbor

    
    def calculateCost(self,ackermannState:AckermannState):
        euclideanCost = ((self.goal[0]- ackermannState.x)**2 + (self.goal[1]- ackermannState.y)**2)**.5
        thetaCost = self.goal[2]-ackermannState.theta
        return euclideanCost# + thetaCost



