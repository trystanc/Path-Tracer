'''
contains basic testing carried out to ensure basic functionality of objects.
'''
import math
import numpy as np
import matplotlib.pyplot as plt
# import matplotlib.pyplot as plt
import optical_elements
from numpy import pi
from ray_module import Ray
import common_functions as cf
#testing ray class
r=Ray([3.,5.,7.],[1/3,2/3,2/3])
print(r.k())
print(r.p())
r.append(r.p(),r.k())
print(r.vertices())
print(r.p(),r.k())
r.p()[0]       

#testing Snell's' law
incident = np.array([np.sqrt(0.5), 0, np.sqrt(0.5)])
normal = np.array([0, 0, -1])
refracted = optical_elements.snells_law(incident, 1, 1.5, normal)
print(refracted)     

#testing a plane lens
ray_list=[]
plane_lens = optical_elements.SphericalRefraction(100,0,1,1.5,100)
output_plane = optical_elements.OutputPlane(103)
ray_list=[Ray([i*6,0,98],[19/20,0,np.sqrt(1-pow(19/20,2))]) 
          for i in range(-4,5)]

for ray in ray_list:
    plane_lens.propagate_ray(ray)
    output_plane.propagate_ray(ray)

cf.plot_rays(ray_list)
#testing a convex lens
ray_list=[]
convex_lens = optical_elements.SphericalRefraction(100,0.03,1,1.5,32)
output_plane = optical_elements.OutputPlane(200)
ray_list=[Ray([i*6,0,0],[0,0,1]) for i in range(-4,5)]
for ray in ray_list:
    convex_lens.propagate_ray(ray)
    output_plane.propagate_ray(ray)
cf.plot_rays(ray_list)

#testing a concave lens
ray_list=[]
concave_lens = optical_elements.SphericalRefraction(100,-0.03,1,1.5,32)
output_plane = optical_elements.OutputPlane(200)
ray_list=[Ray([i*6,0,0],[0,0,1]) for i in range(-4,5)]
for ray in ray_list:
    concave_lens.propagate_ray(ray)
    output_plane.propagate_ray(ray)

cf.plot_rays(ray_list)

#ensuring that a ray does not intercept lens if it's aperture radius is too small
ray=Ray([50,0,0], [0,0,1])
lens = optical_elements.SphericalRefraction(100,0.02,1,1.5,45)
output_plane=optical_elements.OutputPlane(200)
lens.propagate_ray(ray)
output_plane.propagate_ray(ray)
print(ray.p(),ray.k())

#testing that a ray will not be propagated
#if it is travelling in the wrong direction
test_ray = Ray([0,0,0],[0,0,-1])
elements = [plane_lens, convex_lens, concave_lens]
for obj in elements:
    obj.propagate_ray(test_ray)
print(test_ray.p())


#testing bundle function
plt.figure(0)
def ray_bundle(radius, direction, pos, rho):
    ray_list=[Ray(pos,direction)]
    
    x0 = pos[0]
    y0 = pos[1]
    z0 = pos[2]
    
    for i in range(rho+1):
        rpos = (i)*radius/rho
        for j in range(6*i):
            theta = 2*pi*j/(6*i)
            x = rpos * np.cos(theta)
            y = rpos* np.sin(theta)
            new_ray = Ray([x+x0, y+y0, z0], direction)
            ray_list.append(new_ray)
    return ray_list
bundle=ray_bundle(5, [0,0,1], [0,0,0],5)
for i in bundle:
    plt.scatter(i.p()[0],i.p()[1],color='red')

plt.gca().set_aspect('equal', adjustable='box')
plt.show()