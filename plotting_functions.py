'''
functions for common plots
'''
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Times New Roman"

#plots path of rays assuming they are in the y = 0 plane
def plot_rays(ray_list):
    for ray in ray_list:
        
        points = ray.vertices()
        plt.plot([i[2] for i in points],
                 [j[0] for j in points],
                 color = 'red')
    plt.ylabel('x (mm)')
    plt.xlabel('z (mm)') 
    plt.grid(ls = '-.')
    plt.show()

#creates spot diagram for constant z
def spot_diagram(bundle):
    for ray in bundle:
        plt.scatter(ray.p()[0],
                    ray.p()[1],
                    color = 'red')
    plt.xlabel('x (mm)')
    plt.ylabel('y (mm)')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()
        

