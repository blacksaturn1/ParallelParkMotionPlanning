from abc import ABC, abstractmethod
import pygame

class Robot(ABC):
    
    @abstractmethod
    def draw(self,map:pygame.Surface):
        pass
    
    @abstractmethod
    def move(self,event=None):
        pass

    @abstractmethod
    def get_write_info(self):
        pass
