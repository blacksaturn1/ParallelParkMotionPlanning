from typing import List, Optional, Tuple

class AckermannState():

    def __init__(
        self,
        xy: Tuple[float, float],
        theta: float,
        psi: float,
        v: float
    ):
        self.x = xy[0]
        self.y = xy[1]
        self.theta = theta
        self.psi = psi
        self.v=v
    
    def __hash__(self):
        return hash((self.x, self.y,self.psi,self.v))
    
    def __eq__(self, other):
        return (self.x, self.y,self.psi,self.v) == (other.x, other.y,other.psi,other.v)