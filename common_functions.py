'''
functions used across multiple files
'''
import matplotlib.pyplot as plt
import sympy
plt.rcParams["font.family"] = "Times New Roman"

#plots the x and z paths of a ray in a list
def plot_rays(ray_list, title='_'):
    fig, ax = plt.subplots()

    for ray in ray_list:
        
        points = ray.vertices()
        ax.plot([i[2] for i in points],
                 [j[0] for j in points],
                 color = 'red')
    ax.set_ylabel('x (mm)')
    ax.set_xlabel('z (mm)') 
    ax.grid(ls = '-.')
    fig.savefig(f'plots/{title}')


#creates spot diagram with constant z for a bundle
def spot_diagram(bundle, title = '_'):
    fig, ax = plt.subplots()
    for ray in bundle:
        plt.scatter(ray.p()[0],
                    ray.p()[1],
                    color = 'red')
    ax.set_xlabel('x (mm)')
    ax.set_ylabel('y (mm)')
    ax.set_aspect('equal', adjustable='box')
    plt.savefig(f'plots/{title}')


#finds intersection of 2 rays based on the last two vertices
def intersection(ray1, ray2):
    points_1 = ray1.vertices()
    points_2 = ray2.vertices()
   #uses sympy to create lines based on these coordinates
    A = sympy.Point(points_1[-2][0] , points_1[-2][2])
    B = sympy.Point(points_1[-1][0] , points_1[-1][2])
    
    C = sympy.Point(points_2[-2][0] , points_2[-2][2])
    D = sympy.Point(points_2[-1][0] , points_2[-1][2])

    #then finds intersection
    line_1 = sympy.Line(A,B)
    line_2 = sympy.Line(C,D)
    point = line_1.intersection(line_2)
    return float(point[0].y)     

