'''
contains investigations not necessarily listed in script
'''
import math
import numpy as np
import matplotlib.pyplot as plt
import optical_elements
import sympy
import common_functions as cf
from ray_module import Ray

'''
Finding relationship between distance of a ray from the z-axis and its
focal length
'''
lens = optical_elements.SphericalRefraction(100, 0.03, 1, 1.5, 1/0.03)
output_plane=optical_elements.OutputPlane(250)
ray_list=[Ray([0,0,0],[0,0,1])]
z_distance_sq=[]

#directing a set of paraxial rays in the y=0 plane at the lens
for i in range(10):
    ray = Ray([(i+1),0, 0], [0, 0, 1])
    z_distance_sq.append( (i+1)**2)
    ray_list.append(ray)
#propagating rays and then plotting them
for ray in ray_list:
    lens.propagate_ray(ray)
    output_plane.propagate_ray(ray)
#plotting the list of rays
cf.plot_rays(ray_list, title = 'Figure 2')

    

#finds focal length of each ray in ray_list

abberations = []
for i in ray_list[1:]:
    focal_length = cf.intersection(ray_list[0] , i)
    abberations.append(focal_length)
#printing r shows that magnitude of r >0.999, suggesting good fit
r=np.corrcoef(z_distance_sq, abberations)
plt.figure(0)
plt.plot(z_distance_sq, 
        abberations,
        label='Correlation Coefficent r = 0.999')
        
plt.xlabel('Distance of incoming ray from optical axis squared(mm$^{2})$')
plt.ylabel('Distance from paraxial focal point(mm) ')
plt.savefig('plots/Figure 4')
r=np.corrcoef(z_distance_sq,abberations)
plt.legend()
plt.grid()


#plot showing abberations when rays aren't paraxial
ray_list = []

for i in range(-5, 6):
    ray = Ray([3*(i+1),0, 0], [0, 0, 1])
    ray_list.append(ray)
for ray in ray_list:
    lens.propagate_ray(ray)
    output_plane.propagate_ray(ray)

cf.plot_rays(ray_list, title='Figure 3')

'''
comparing bundle diameter of different sizes' rms spot radius
to diffraction limit. Using PlanoConvex Lenses from task 15.
'''
#this is data generated from raytracer.py, but moving it here avoids having
#to run raytracer every time I run this file.
pc_rms_list_1 = [0.00029423290710465735, 
                 0.00235756074079178, 
                 0.00797667013127287, 
                 0.01897388151175431, 
                 0.0372261141162458]

pc_rms_list_2 = [7.423444498598843e-05, 
                 0.000594362559675203, 
                 0.002008776806444387, 
                 0.004770901978528613, 
                 0.009341799120645821]

focal_point  = 198.45281275318274


bundle_diameter = [2*i for i in range(1,6)]
#assuming a wavelength of 588nm
wavelength = 588e-6

def diffraction_limit(diameter):
    return focal_point * wavelength/ diameter
plt.figure(3)

#plots the diffraction limit against the spot radius for both lens
#configurations
plt.plot(bundle_diameter,
         pc_rms_list_1,
         label = 'Convex Part Facing Away From Input',
         color = 'purple')
plt.plot(bundle_diameter,
          [diffraction_limit(i) for i in bundle_diameter],
          label = 'Diffraction Limit',
          color = 'green')
plt.plot(bundle_diameter,
         pc_rms_list_2,
         label = 'Convex Part Facing Toward Input')

plt.xlabel('Bundle Diameter (mm)')
plt.ylabel('Length (mm)')
plt.title('Size of Geometrical Focus vs Diffraction Limit', fontsize = '15')
plt.legend()
plt.grid()
plt.savefig('plots/Figure 7')

  

    






