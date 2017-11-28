import mpmath as mp
import matplotlib.pyplot as plt

'''
The class Line represents a geometric line with point and slope
'''
class Line():

    # constructor
    #  point - a point on the line
    #  angle - the direction that the line is pointing (ccw from +ve x-axis)
    def __init__(self, point, angle):

        vec_x = mp.cos(angle)
        vec_y = mp.sin(angle)
        new_x = point[0] + 3*vec_x 
        new_y = point[1] + 3*vec_y

        self.point = point          # Point on the line
        self.vec   = [vec_x, vec_y] # Direction Vector
        self.angle = angle          # The angle of the direction vector
        self.newPoint    = [new_x, new_y] # The eq for graphing purposes 

    # evaluate_x(x)
    #  x - the x coordinate
    # returns the (x,y) coordinate on the line 
    def evaluate_x(self, x):

        time_factor = (x - self.point[0]) / self.vec[0]

        return [x, self.point[1] + time_factor * self.vec[1]]

    # evaluate_y(y)
    #  y - the y coordinate
    # returns - (x,y) coordinate on the line 
    def evaluate_y(self, y):

        time_factor = (y - self.point[1]) / self.vec[1]

        return [self.point[0] + time_factor * self.vec[0], y]
    
    # intersection(line)
    #  line - some line
    # returns - False if self and line are parallel
    #           else (x,y) coordinate of the intersection between line and self
    def intersection(self, line):

        # Solve for x
        # ax + b = cx + d
        # x = (d - b)/(a - c)

        # Useful Variables
        a = self.evaluate_x(1) - self.evaluate_x(0)
        b = self.evaluate_x(0)
        c = line.evaluate_x(1) - self.evaluate_x(0)
        d = line.evaluate_x(0)

        # lines parallel so no intersection
        if a == c:
            return False

        x_val_intersection = (d - b)/(a - c)

        return [x_val_intersection, self.evaluate_x(x_val_intersection)]
    
    # angle_between(line)
    #  line - some line
    # returns - the ccw angle from self to line
    def angle_between(self, line):
        
        l1_vec = self.vec
        l2_vec = line.vec

        dot_vec = l1_vec[0] * l2_vec[0] + l1_vec[1] * l2_vec[1]
        det_vec = l1_vec[0] * l2_vec[1] - l1_vec[1] * l2_vec[0]

        return mp.atan2(det_vec, dot_vec)

'''
The class Circle represents a geometric circle with center and radius
'''
class Circle():

    # constructor
    #  center - the (x,y) coordinate of the circle center
    #  radius - the radius of the circle
    def __init__(self, center, radius):
        self.center = center # The center of the circle
        self.radius = radius # The radius of the circle
        self.eq     = plt.Circle(center, radius) # The eq for graphing purposes

    # evaluate_x(x)
    #  x - some x coordinate
    # returns - the (x,y) coordinate on the circle
    def evaluate_x(self, x):

        root = mp.sqrt(self.radius**2 - (x - self.center[0])**2)

        return [[x, self.center[1] - root], [x, self.center[1] + root]]

    # evaluate_y(y)
    #  y - some y coordinate
    # returns - the (x,y) coordinate on the circle
    def evaluate_y(self, y):

        root = mp.sqrt(self.radius**2 - (y - self.center[1])**2)

        return [[self.center[0] - root, y], [self.center[0] + root, y]]

    # intersection(line)
    #  line - some line
    # returns - a list of (x,y) coordinates of intersection points between self and line
    def intersection(self, line):

        # Solve for x
        # common values after line equaltion subbed into circle
        # (x - c_x)^2 + (line_slope*x + constant)^2 = r^2 
        line_slope = line.evaluate_x(1)[1] - line.evaluate_x(0)[1]
        constant = line.evaluate_x(0)[1] - self.center[1]
        r_2 = self.radius**2
        c_x = self.center[0]

        # Find coefficients of polynomial
        x2_coeff = (line_slope + 1)**2
        x1_coeff = - 2 * (line_slope*constant + c_x)
        x0_coeff = c_x**2 + constant**2 - r_2

        # Solve using quadratic formula
        disc = x1_coeff**2 - 4 * x2_coeff * x0_coeff # discriminant

        x_val_intersections = []

        if disc == 0:
            x1 = -x1_coeff / (2*x2_coeff)
            x_val_intersections = [x1.real]
        else:
            x1 = (-x1_coeff + mp.sqrt(disc)) / (2*x2_coeff)
            x2 = (-x1_coeff - mp.sqrt(disc)) / (2*x2_coeff)
            x_val_intersections = [x1.real,x2.real]

        print(x_val_intersections)

        # transform to [x,y] coordinate form
        return [line.evaluate_x(x) for x in x_val_intersections]
    
    # reflection(line)
    #  line - some line
    # returns - False if the circle does not intersect with the line
    #           a new line that is the reflection of line off of the circle surface
    def reflection(self, line):

        # find intersection point if it exists
        intersection_point = self.intersection(line) 

        # Cull so we take the closest intersection point
        if len(intersection_point) == 0:
            return [False, line.newPoint]
        elif len(intersection_point) == 2:
            distance_1 = abs(intersection_point[0][0] - line.point[0])
            distance_2 = abs(intersection_point[1][0] - line.point[0])

            if distance_1 > distance_2:
                intersection_point = intersection_point[1]
            else:
                intersection_point = intersection_point[0]
        else:
            intersection_point = intersection_point[0]

        # find the norm of the circle at the intersection point with direction reversed
        #  need to match the direction of line inorder to get the inner angle
        delta_x = - (intersection_point[0] + self.center[0])
        delta_y = - (intersection_point[1] + self.center[1])
        angle   = mp.atan2(delta_y, delta_x)
        norm    = Line(intersection_point, angle)

        # find the line between the center of the circle and line source
        delta_x = line.point[0] - self.center[0]
        delta_y = line.point[1] - self.center[1]
        angle   = mp.atan2(delta_y, delta_x)
        ls_to_c = Line(self.center, angle)        

        # Useful angles to have
        # theta - absolute angle between norm and line
        # base  - angle of the ls_to_c line
        # phi   - angle between line and ls_to_c line
        theta = abs(norm.angle_between(line))
        base  = ls_to_c.angle
        phi   = ls_to_c.angle_between(line)

        # The angle of the reflection is equal to
        # if phi > 0 then angle = base - ( pi - 2*theta + abs(phi))
        # else            angle = base + ( pi - 2*theta + abs(phi))
        if phi > 0:
            angle = base - ( mp.pi - 2*theta + abs(phi))
        else:
            angle = base + ( mp.pi - 2*theta + abs(phi))

        return [True, intersection_point, angle]
