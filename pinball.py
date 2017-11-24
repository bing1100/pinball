import sympy as sp
import sympy.geometry as spg 
import sympy.plotting as spp
import mpmath as mp
from sympy import symbols
import matplotlib.pyplot as mpp

#Starting ray
start_p1 = spg.Point(0,0)

ax=mpp.gca()
start = spg.Ray(start_p1,angle=mp.pi/4)

CD_CR_RATIO = 3


has_escaped = False
newRay = start
whichCircle = 1

n_reflection = 0

C_xPoint = sp.sqrt(sp.Pow(CD_CR_RATIO,2)
                    - sp.Pow(CD_CR_RATIO/2,2))

C1_Cen = [0,0]
C2_Cen = [C_xPoint, CD_CR_RATIO/2]
C3_Cen = [C_xPoint, -CD_CR_RATIO/2]

def create_circle_sym(centre, radius):
    p = spg.Point(centre[0],centre[1])
    return spg.Circle(p, radius)

C1_sym = create_circle_sym(C1_Cen,1)
C2_sym = create_circle_sym(C2_Cen,1)
C3_sym = create_circle_sym(C3_Cen,1)

all_circles = [mpp.Circle(C1_Cen,1), mpp.Circle(C2_Cen,1),mpp.Circle(C3_Cen,1)]

def create_line_graph(point1, point2):
    p1 = spg.Point(point1[0], point1[1])
    p2 = spg.Point(point2[0], point2[1])
    return spg.Ray(p1,p2)

def has_intersection_sym(circle, ray):
    r_source = ray.source

    intersection_points = circle.intersection(ray)

    if len(intersection_points) != 2:
        return [False]
    else:
        if r_source.distance(intersection_points[0]) > r_source.distance(intersection_points[1]):
            print(str(float(intersection_points[1].x)) + " " + str(float(intersection_points[1].x)))
            return [True,intersection_points[1]]
        else:

            print(str(float(intersection_points[0].x)) + " " + str(float(intersection_points[0].x)))
            return [True,intersection_points[0]]
    

def find_reflected_ray_sym(circle, ray, intersection):
    r_source = ray.source
    c_centre = circle.center

    line = spg.Line(intersection,c_centre)

    shift_angle = float(line.angle_between(ray))

    inter_centered = intersection - r_source
    cente_centered = - c_centre - r_source

    dot_vec = inter_centered.x * cente_centered.x + inter_centered.y * cente_centered.y
    det_vec = inter_centered.x * cente_centered.y + inter_centered.y * cente_centered.x 

    print("dot: " + str(float(dot_vec)) + " det: " + str(float(det_vec)))

    ray_center_angle = mp.atan2(float(det_vec), float(dot_vec))

    if ray_center_angle < mp.pi:
        return spg.Ray(intersection, angle = 2*shift_angle - sp.Abs(mp.pi - ray_center_angle))
    else:
        return spg.Ray(intersection, angle = -(2*shift_angle - sp.Abs(mp.pi - ray_center_angle)))

def show_shapes(patchs):

    for patch in patchs:
        ax.add_patch(patch)
    mpp.axis('scaled')
    mpp.grid(True)
    mpp.show()

def reflection_stepper(circle_num,circle,intersect):
    global newRay, ax, whichCircle
    x = [newRay.source.x]
    y = [newRay.source.y]
    newRay = find_reflected_ray_sym(circle, newRay, intersect)
    x = x.append(newRay.source.x)
    y = y.append(newRay.source.y)
    print(x + "\n")
    print(y)
    whichCircle = circle_num
    ax.plot(x,y, marker='o')

while(n_reflection <= 1 and not has_escaped):

    n_reflection += 1
    print(n_reflection)

    print(newRay)

    if whichCircle == 1:

        p1 = newRay.source

        C2_intersect = has_intersection_sym(C2_sym, newRay)
        C3_intersect = has_intersection_sym(C3_sym, newRay)

        if C2_intersect[0]:
            reflection_stepper(2, C2_sym, C2_intersect[1])
            
        elif C3_intersect[0]:
            reflection_stepper(3, C3_sym, C3_intersect[1])
        else:
            has_escaped = True
        

        

    elif whichCircle == 2:
        
        p1 = newRay.source

        C1_intersect = has_intersection_sym(C1_sym, newRay)
        C3_intersect = has_intersection_sym(C3_sym, newRay)

        if C1_intersect[0]:
            reflection_stepper(1, C1_sym, C1_intersect[1])
        elif C3_intersect[0]:
            reflection_stepper(3, C3_sym, C3_intersect[1])
        else:
            has_escaped = True
    else:
        
        p1 = newRay.source

        C1_intersect = has_intersection_sym(C1_sym, newRay)
        C2_intersect = has_intersection_sym(C2_sym, newRay)

        if C1_intersect[0]:
            reflection_stepper(1, C1_sym, C1_intersect[1])
        elif C2_intersect[0]:
            reflection_stepper(2, C2_sym, C2_intersect[1])
        else:
            has_escaped = True

show_shapes(all_circles)