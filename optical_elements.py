'''
This module contains all the optical elements Classes in here. 
Includes spherical lens (extended to include plane
lenses as well) and  output plane classes.

'''



import numpy as np
import math


def normal_of(vector):
    return vector/np.linalg.norm(vector)

#returns unit vector of a waveafter refraction 
#note k1 and n need to be passed as unit vectors
def snells_law(k1, n1 ,n2, n):
    #in case ray is parallel to surface normal
    if math.isclose(( np.dot(k1,n))**2 , 1):
        return k1
   
    cos_theta1 = np.dot(n, k1)
    sin_theta1 = np.sqrt(1 - cos_theta1**2) 
   
    if sin_theta1 > (n2/n1):
        return None     
#uses snells' law to find angle between new direction and surface normal 
    sin_theta2 = n1*sin_theta1/n2
    cos_theta2 = np.sqrt(1 - sin_theta2**2)

#finds k2 in terms of components perpendicular 
#and parallel to lens surface
    
    plane_normal = np.cross(n, k1)
    parallel = normal_of( np.cross(plane_normal, n) )
    k2 = cos_theta2*n + sin_theta2*parallel
    return k2

class OpticalElement:
#base class used to make more specific optical elements
  def propagate_ray(self, ray):
    "propagate a ray through the optical element"
    raise NotImplementedError()

class SphericalRefraction(OpticalElement):
    def __init__(self, z0, curv, n1, n2, aper_rad):
        self._z0 = z0
        self._cur = curv
        self._n1 = n1
        self._n2 = n2
        self._ar = aper_rad
        if curv != 0:
            self._centre = np.array([0, 0, z0 + 1/curv])
        else:
            self._centre = z0

     
    def z0(self):
        return self._z0
    def cur(self):
        return self._cur
    def n1(self):
        return self._n1
    def n2(self):
        return self._n2
    def ar(self):
        return self._ar
    def centre(self):
        return self._centre
   
    
    #calculatues first valid interception of ray and surface
    def  intercept(self, ray):      
        k = ray.k()  
        
        #in the case it is a plane surface
        if self.cur() == 0.:
           l = (self.z0() - ray.p()[2])/k[2]

           intersection = ray.p() + l * ray.k()
           if l > 0. and np.linalg.norm(intersection-[0,0,intersection[2]]) < self.ar():
               return intersection
           else:
               return None
        
        #in case curvature is non zero, solves quadratic in script
        r = ray.p() - self.centre() 
        drk=np.dot(r, k)
        drr=np.dot(r, r)
        R=1/self.cur()
        discrim = (drk)**2 - (drr) + (R)**2
        if discrim < 0.:
            return None
        l1 = -drk - np.sqrt(discrim)
        
        if self.cur() < 0:
            l1 += 2*np.sqrt(discrim)
        if l1 > 0:
            intersection = ray.p() + l1*k
            #checks if aperture radius means the object is not intercepted
            if np.linalg.norm(intersection-[0,0,intersection[2]]) < self.ar():
                return intersection
            else:
                return None
            
            
#uses intercept and the snell's law function to find the
#new direction and position of ray when it hits the surface 
    def propagate_ray(self, ray):
        
        incident = self.intercept(ray)
        if incident is None:
            return None
        k_hat = ray.k()
        
        if self.cur()==0:
            new_k = snells_law(k_hat, self.n1(), self.n2(), np.array([0,0,1]))
            ray.append(incident,new_k)
        
        else:
            n_hat = -1 * normal_of(incident - self.centre())
           #in case ray is convex
            if self.cur()<0:
                new_k = snells_law(k_hat, self.n1(), self.n2(), -1*n_hat)
            else:
                new_k = snells_law(k_hat, self.n1(), self.n2(),n_hat)
           
            if new_k is None:
                return None
            ray.append(incident, new_k)

#output plane is infinitely wide. Only has one data attribute, which is it's
#position on the z axis
class OutputPlane(OpticalElement):
    def __init__(self, zpos):
        self._zpos=zpos
    
    def zpos(self):
        return self._zpos
    
    def intercept(self, ray):
    #l is the length of vector 
        l=(self.zpos() - ray.p()[2])/ray.k()[2]
        #if ray is travelling in the wrong direction
        if l<0:
            return None
        else:
            return ray.p()+l*ray.k()
    
    def propagate_ray(self, ray):
        new_p = self.intercept(ray)
        ray.append(new_p, ray.k())

        
        
    
        


        

     
        
    
