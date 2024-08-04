'''
This module contains the optical ray class. An object of
the ray class is initialised with 2 lists each 
which give both the first point and the unit wave
vector in cartesian coordinates. New points for the ray's path can be 
calculated using its wavevector and its current position, 
and the vertices attribute records all the points it passes through.
colour is a tuple of rgb values from 0 to 1 for the mona lisa plot
'''

import numpy as np
import math


class Ray:


    def __init__(self, p, k, color='red'):
        if len(p) != 3 or len(k) != 3:
            raise TypeError("position/wave vector must be a list of length 3")
        self._p = np.array(p)
        self._k = np.array(k)
        if not math.isclose(np.linalg.norm(self._k), 1.):
            raise ValueError("k must be a unit vector")
        self._vertices = [self._p]   
        self._color=color
    
    
    def p(self):
        return self._p
    def k(self):
        return self._k
    def vertices(self):
        return self._vertices  
    def color(self):
        return self._color
    def append(self, p, k):
        self.vertices().append(p)
        self._p = p
        self._k = k
    
    def __str__(self):
        return f'{self.p()} , {self.k()}'