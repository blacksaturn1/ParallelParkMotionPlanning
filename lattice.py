from ackermannState import AckermannState
from typing import List, Optional, Tuple
import pygame
import math
from ackermann import RobotAckermann
from queue import PriorityQueue
class Lattice:

    def __init__(self,location:Tuple[float,float,float],goal:Tuple[float,float,float],
                 obstacleGrid,robot:RobotAckermann,display, write_info:callable) -> None:
        self.currentLocation=location
        self.goal:Tuple[float,float,float]=goal
        self.neighbors:List[AckermannState]=[]
        self.path: dict[AckermannState,AckermannState]={}
        self.network_path: dict[AckermannState,List[AckermannState]]={}
        self.cost: dict[AckermannState,float]={}
        self.obstacles:list[pygame.Rect] = obstacleGrid
        self.queue:PriorityQueue[AckermannState] = PriorityQueue()
        self.robot = robot
        x,y,theta=self.currentLocation
        self.firstState = AckermannState((x,y),theta,0,0,self.robot.img)
        self.firstState.cost_to_come = 0
        self.firstState.cost_to_go=self.firstState.get_cost(self.goal)
        self.currentState = self.firstState
        # previousState.cost_to_come = 0
        # previousState.cost_to_go=previousState.get_cost(self.goal)
        self.lastState=None
        self.display = display
        self.write_info=write_info
        

    def add_neighbors(self, neighbors):
        self.neighbors=[]
        for neighbor in neighbors:
            if self.isCollision(neighbor):
                continue
            self.neighbors.append(neighbor)

    def search(self):
        cost = 9999
        x,y,theta=self.currentLocation
        previousLocation=self.currentLocation
        startState = self.firstState
        lowestCostState=startState
        self.queue.put(startState)
        state=startState
        # neighbors = self.robot.get_neighbors(self.currentLocation)
        # for nextState in neighbors:
        #         self.path[nextState]=previousState
        counter=0
        while not self.goalCheck(state) and self.queue.not_empty:
            counter+=1
            self.write_info("Planner iteration: {}".format(counter))
            state = self.queue.get()
            # state.cost_to_come=state.get_cost(previousLocation)
            # state.cost_to_go=state.get_cost(self.goal)
            cost = state.cost_to_go
            # if cost_to_go>cost:
            #     continue
            
            if state.cost_to_go<lowestCostState.cost_to_go:
                lowestCostState=state
                if state.cost_to_go>500:
                    self.robot.maxspeed=220
                elif state.cost_to_go>200:
                    self.robot.maxspeed=40
                    self.robot.dt=.5
                elif state.cost_to_go>50:
                    self.robot.maxspeed=30
                    self.robot.dt=.5
                elif state.cost_to_go>15:
                    self.robot.maxspeed=10
                    self.robot.dt=.5

            state_location = state.get_location()
            neighbors = self.robot.get_neighbors(state_location)
            # self.network_path[state]=[]#.extend(neighbors)
            # self.network_path[state].extend(neighbors)
            for nextState in neighbors:
                reward = 5
                if nextState.v<0:
                    reward = 6
                nextState.cost_to_come = (state.cost_to_come+
                                          nextState.get_cost(state_location))
                nextState.cost_to_go=nextState.get_cost(self.goal)*reward
                # if nextState.cost_to_go>cost:
                #     continue
                if self.isCollision(nextState):
                    continue
                if nextState not in self.path:
                    self.path[nextState]=state
                    self.queue.put(nextState)
                    position = nextState.xy
                    self.display.fill((0, 255, 0), (position, (2, 2)))
                    pygame.event.get()
                    pygame.display.update()
            if counter >1 and counter%500==0:
                break
            ##self.queue.extend(neighbors)
        # self.lastState = lowestCostState
        self.lastState = state
        return state
        # return lowestCostState

    def goalCheck(self,state:AckermannState):
        distanceToGoal = self.calculateCostToGoal(state)
        thetaDiff = abs(self.goal[2]-state.theta)
        return distanceToGoal<=5 and thetaDiff<=(math.pi/8)


    def plan(self):
        for neighbor in self.neighbors:
            self.cost[neighbor]=self.calculateCost(neighbor)

    def isCollision(self,state:AckermannState):
        for obstacle in self.obstacles:
            if obstacle.colliderect(state.rect):
                return True
        return False
    
    def step(self):
        lowestCost=9999
        lowestCostNeighbor=None
        for state,value in self.cost.items():
            if value<lowestCost:
                if not self.isCollision(state):
                    lowestCost=value 
                    lowestCostNeighbor=state
        self.cost={}
        self.neigbors={}
        return lowestCostNeighbor

    def step2(self):
        if self.currentState is None:
            return None
        if self.currentState==self.lastState:
            return None
        
        currentState = self.lastState
        previousState = currentState

        while previousState!=self.currentState:
            currentState=previousState
            previousState=self.path[currentState]
            
            
        # for state,value in self.cost.items():
        #     if value<lowestCost:
        #         if not self.isCollision(state):
        #             lowestCost=value
        #             lowestCostNeighbor=state
        # self.cost={}
        # self.neigbors={}
        self.currentState=currentState
   
        return currentState
    
    def calculateCostToGoal(self,ackermannState:AckermannState):
        euclideanCost = ((self.goal[0]- ackermannState.x)**2 + (self.goal[1]- ackermannState.y)**2)**.5
        # thetaCost = abs(self.goal[2]-ackermannState.theta)
        return euclideanCost #+ thetaCost



