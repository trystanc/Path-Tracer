"""
Main Script tasks are all plotted here.
"""
import math
import numpy as np
import optical_elements as oe
from scipy.optimize import fmin_tnc
import common_functions as cf
from numpy import pi
from ray_module import Ray

        
'''
task 9
'''
#plotting some example rays with an arbitrary direcction at lens
lens = oe.SphericalRefraction(100, 0.03, 1, 1.5, 32)
output_plane = oe.OutputPlane(250)
example_k = [-0.1,0,np.sqrt(1-(0.1**2))]
example_rays = [Ray([i*7,0,0],  example_k) for i in range(-6,7)]

for ray in example_rays:
    lens.propagate_ray(ray)
    output_plane.propagate_ray(ray)
cf.plot_rays(example_rays, 'Figure 1')






'''
task 10
'''

parallel_rays = [Ray([i*6,0,0], [0,0,1]) for i in range(-3,4)]

for ray in parallel_rays:
    lens.propagate_ray(ray)
    output_plane.propagate_ray(ray)

cf.plot_rays(parallel_rays, 'Figure 10')


# uses sympy to create line based on two points created by line vertices and
# then find their intersection. Used to find the paraxial focal point.


#finding paraxial focus point of lens

central_ray = Ray([0, 0 ,0], [0, 0, 1])
paraxial_ray = Ray([0.1, 0, 0], [0, 0 ,1])
lens.propagate_ray(central_ray)
output_plane.propagate_ray(central_ray)
lens.propagate_ray(paraxial_ray)
output_plane.propagate_ray(paraxial_ray)

print('(Task 10): focal point of lens for ray at x=0.1mm is at z=',
      cf.intersection(central_ray, paraxial_ray),
      'mm so paraxial focal length is 100 mm')

'''
Task 11
If there is a point source of rays further
than the focal length from lens, then a real image will be produced.
Each point source's rays must converge to the same point.
'''
##formation of real image
point_rays = [Ray([0, 0, 0], 
        [i*0.01, 0, np.sqrt(1-(i*0.01)**2)]) 
        for i in range(-2,3) ]
output_plane = oe.OutputPlane(400)
for ray in point_rays:
    lens.propagate_ray(ray)
    output_plane.propagate_ray(ray)

cf.plot_rays(point_rays, 'Figure 5')

#formation of virtual image
point_rays = [Ray([0, 0, 70], 
        [i*0.01, 0, np.sqrt(1-(i*0.01)**2)]) 
        for i in range(-2,3) ]
for ray in point_rays:
    lens.propagate_ray(ray)
    output_plane.propagate_ray(ray)

cf.plot_rays(point_rays, 'Figure 6')
         
'''
Tasks 12-14
'''
#returns a list of rays all pointing in the same direction in a concentric
#circle. 'rho' is the ray density and controls the number of concentric circles
def ray_bundle(radius, direction, pos, rho):
    
    ray_list=[Ray(pos,direction)]
    x0 = pos[0]
    y0 = pos[1]
    z0 = pos[2]
 #finds position of each ray in bundle in polar coordinates, and then converts
#to cartesian
    for i in range(rho+1):
        rpos = (i)*radius/rho
        for j in range(6*i):
            theta = 2*pi*j/(6*i)
            x = rpos * np.cos(theta)
            y = rpos* np.sin(theta)
            new_ray = Ray([x+x0, y+y0, z0], direction)
            ray_list.append(new_ray)
    
    return ray_list

output_plane = oe.OutputPlane(200)
bundle=ray_bundle(2.5, [0,0,1], [0,0,0], 10)
cf.spot_diagram(bundle, 'Figure 11')


dist_arr=[]
for ray in bundle:
    
    lens.propagate_ray(ray)
    output_plane.propagate_ray(ray)
    distsq = (ray.p()[0])**2 + (ray.p()[1])**2
    dist_arr.append(distsq)

cf.plot_rays(bundle, 'Figure 16')
cf.spot_diagram(bundle, 'Figure 12')
rms = np.sqrt(np.mean(dist_arr))
print('(Task 13): size of geometrical focus:',rms, 'mm')



'''
task15
'''

#finding paraxial focus by propagating a  parxial ray

aperture_radius = np.sqrt(50**2 - 45**2)
plane_part = oe.SphericalRefraction(100, 0, 1, 1.5168, aperture_radius)
convex_part = oe.SphericalRefraction(105, -0.02, 1.5168, 1, aperture_radius)
output_plane = oe.OutputPlane(400)
ray = Ray([0.01,0,0], [0, 0, 1])
elements = [plane_part, convex_part, output_plane]

for obj in elements:
    obj.propagate_ray(ray)
cf.plot_rays([ray], title = 'Figure 13')

plane_ray=Ray([0,0,0], [0,0,1])
plane_ray.append([0,0,400], [0,0,1])
focal_point = cf.intersection(ray, plane_ray)



#finding size of geometrical focus with ray bundles up to 10mm

elements[2] = oe.OutputPlane(focal_point)
bundle_list = [ray_bundle(i, [0 ,0 ,1], [0, 0, 0], 10) for i in range(1,6)]

for obj in elements:
    for bundle in bundle_list:
        for ray in bundle:
            obj.propagate_ray(ray)


pc_rms_list_1 = []

for bundle in bundle_list:
    dist_sq = []
    for ray in bundle:
        dist_sq.append((ray.p()[0])**2 + (ray.p()[1])**2)
    dist_arr = np.array(dist_sq)
    new_rms = (np.sqrt(np.mean(dist_arr)))
    pc_rms_list_1.append(new_rms)


#now for the convex part facing the other way

plane_part = oe.SphericalRefraction(105, 0, 1.5168, 1, aperture_radius)
convex_part = oe.SphericalRefraction(100, 0.02, 1, 1.5168, aperture_radius)
output_plane = oe.OutputPlane(400)

#first finding the focal plane
ray = Ray( [0.01,0,0], [0, 0, 1])
elements = [convex_part, plane_part, output_plane]

for obj in elements:
    obj.propagate_ray(ray)



plane_ray=Ray([0, 0, 0], [0, 0, 1])
plane_ray.append([0, 0, 400], [0, 0, 1])
focal_point = cf.intersection(ray, plane_ray)

cf.plot_rays([ray],'Figure 14')

#now to find the size of geometrical foci
elements[2] = oe.OutputPlane(focal_point)                
pc_rms_list_2 = []
bundle_list = [ray_bundle(i, [0,0,1], [0, 0, 0], 10) for i in range(1,6)]

for obj in elements:
    for bundle in bundle_list:
        for ray in bundle:
            obj.propagate_ray(ray)

for bundle in bundle_list:
    dist_sq = []
    for ray in bundle:
        dist_sq.append([(ray.p()[0])**2 + (ray.p()[1])**2])
    dist_arr = np.array(dist_sq)
    new_rms = np.sqrt( np.mean(dist_arr) )
    pc_rms_list_2.append(new_rms)


print('Task 15(Geometrical spot size for bundle radii from 1-5 for both lenses):',
      pc_rms_list_1, 
      pc_rms_list_2)
'''
lens Optimisation
'''
#take curvatures of the two parts of the lens in a list and calculates
#the resulting rms of spot diagram for a bundle with a diameter of 10mm
#will be minimised to find curvatures
def rms_of_lens(curvatures, focal_point = 200):
    
    lens_1 = oe.SphericalRefraction(100, curvatures[0], 1, 1.5168, 20)
    lens_2 = oe.SphericalRefraction(105, curvatures[1], 1.5168, 1, 20)
    output_plane=oe.OutputPlane(focal_point)


    elements = [lens_1, lens_2, output_plane]
    bundle = ray_bundle(5, [0, 0, 1], [0, 0, 0], 10)

    for obj in elements:
        for ray in bundle:
            obj.propagate_ray(ray)
#calculate the square of the distance
    dist_squares = [] 
    
    for ray in bundle:
        dist_squares.append((ray.p()[0])**2 + (ray.p()[1])**2)
#finding the square root of the mean of the squares
    dist_arr = np.array(dist_squares)
    bicon_rms = (np.sqrt(np.mean(dist_arr)))
    return bicon_rms

#now to find the optimal curvatures
initial_guess = [0.1, -0.1]

opt_curvs,_,_=fmin_tnc(rms_of_lens, 
                       initial_guess, 
                       approx_grad = True,
                       bounds = [(0,0.2), (-0.2, 0)],
                       disp=0,
                       args=[200])

print('Optimised Lens Curvatures:',opt_curvs)
print('Size of Geometrical Focus for Optimised Lens:', 
      rms_of_lens(opt_curvs, 200))

#plotting the spot diagram for these optimised curvatures
last_bundle = ray_bundle(5, [0,0,1], [0,0,0], 10)

optimised_lens_1 = oe.SphericalRefraction(100, opt_curvs[0], 1, 1.5168, 20)
optimised_lens_2 = oe.SphericalRefraction(105, opt_curvs[1], 1.5168, 1, 20)
output_plane = oe.OutputPlane(200)

for ray in last_bundle:
    optimised_lens_1.propagate_ray(ray)
    optimised_lens_2.propagate_ray(ray)
    output_plane.propagate_ray(ray)

cf.spot_diagram(last_bundle, title = 'Figure 15')


          
            
        
    
            
            
            
        
    
        
    
        
    
   


    
        
    
        

    
    
    
    


