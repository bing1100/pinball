import sympy as sp
import sympy.geometry as spg 
from sympy import symbols
import matplotlib.pyplot as plt

CD_CR_RATIO = 3

C_xPoint = sp.sqrt(sp.Pow(CD_CR_RATIO,2)
                    - sp.Pow(CD_CR_RATIO/2,2))

C1_Cen = (0,0)
C2_Cen = (C_xPoint, CD_CR_RATIO/2)
C3_Cen = (C_xPoint, -CD_CR_RATIO/2)

def create_ray_sym(point1, point2):
    p1 = spg.Point(point1[0], point1[1])
    p2 = spg.Point(point2[0], point2[1])
    return spg.Ray(p1,p2)

def find_reflected_line_sym(circle, ray):
    c_center = circle.center
    intersection_points = spg.intersection(circle,ray)
    if len(intersection_points) != 2:
        return False

    norm = spg.Ray(c_center, intersection_points[0])

    newPoint = ray.source.reflect(norm)

    return spg.Ray(intersection_points[0], newPoint)

def find_intersection_sym(shapes):
    points = spg.intersection(shapes)
    return [[point.x, point.y] for point in points]

def create_circle_sym(centre, radius):
    p = spg.Point(centre[0],centre[1])
    return spg.Circle(p, radius)

def create_circle_plot(centre, radius):
    return plt.Circle(centre, radius, fill=False)

def show_shapes(patchs):
    ax=plt.gca()
    for patch in patchs:
        ax.add_patch(patch)
    plt.axis('scaled')
    plt.grid(True)
    plt.show()

p = find_reflected_line_sym(create_circle_sym(C1_Cen,1), create_ray_sym((0,3),(0.5,0)))

print(p.source.x + " " + p.source.y)