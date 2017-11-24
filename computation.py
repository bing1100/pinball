import mpmath as mp

class Line():

    def __init__(self, point, angle):

        mod_angle = (angle + mp.pi/2) % (2*mp.pi)
        step_x_coord = -1 if mod_angle >= mp.pi else 1
        step_y_coord = step_x_coord * mp.sin(angle) 

        self.point = point
        self.step_shift =[step_x_coord, step_y_coord]
        self.angle = angle

    def evaluate_x(self, x):

        time_factor = (x - self.point[0]) / self.step_shift[0]

        return [x, self.point[1] + time_factor * self.step_shift[1]]

    def evaluate_y(self, y):

        time_factor = (y - self.point[1]) / self.step_shift[1]

        return [self.point[0] + time_factor * self.step_shift[0], y]

    def intersection(self, line):

        # Solve for x
        # ax + b = cx + d
        # x = (d - b)/(a - c)

        # useful variables
        a = self.evaluate_x(1) - self.evaluate_x(0)
        b = self.evaluate_x(0)
        c = line.evaluate_x(1) - self.evaluate_x(0)
        d = line.evaluate_x(0)

        x_val_intersection = (d - b)/(a - c)

        return [x_val_intersection, self.evaluate_x(x_val_intersection)]

    def angle_between(self, line):
        
        l1_vec = self.step_shift
        l2_vec = line.step_shift

        dot_vec = l1_vec[0] * l2_vec[0] + l1_vec[1] * l2_vec[1]
        det_vec = l1_vec[0] * l2_vec[1] + l1_vec[1] * l2_vec[0]

        return mp.atan2(det_vec, dot_vec)

class Circle():

    def __init__(self, center, radius):

        self.center = center
        self.radius = radius

    def evaluate_x(self, x):

        root = mp.sqrt(self.radius**2 - (x - self.center[0])**2)

        return [[x, self.center[1] - root], [x, self.center[1] + root]]

    def evaluate_y(self, y):

        root = mp.sqrt(self.radius**2 - (y - self.center[1])**2)

        return [[self.center[0] - root, y], [self.center[0] + root, y]]


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
            x_val_intersections = [x1]
        else:
            x1 = (-x1_coeff + mp.sqrt(disc)) / (2*x2_coeff)
            x2 = (-x1_coeff - mp.sqrt(disc)) / (2*x2_coeff)
            x_val_intersections = [x1,x2]

        # transform to [x,y] coordinate form
        return [[x, line.evaluate_x(x)] for x in x_val_intersections]

    def reflection(self, line):

        # find intersection point if it exists
        intersection_point = self.intersection(line)

        # Cull so we take the closest intersection point
        if len(intersection_point) == 0:
            return line
        elif len(intersection_point) == 2:
            distance_1 = abs(intersection_point[0][0] - line.point[0])
            distance_2 = abs(intersection_point[1][0] - line.point[0])

            if distance_1 > distance_2:
                intersection_point = intersection_point[1]
            else:
                intersection_point = intersection_point[0]
        else:
            intersection_point = intersection_point[0]

        # find the norm of the circle at the intersection point
        delta_x = intersection_point[0] - self.center[0]
        delta_y = intersection_point[1] - self.center[1]
        angle   = mp.atan2(delta_y, delta_x)
        norm    = Line(intersection_point, angle)

        # find the line between the center of the circle and line source
        delta_x = line.point[0] - self.center[0]
        delta_y = line.point[1] - self.center[1]
        angle   = mp.atan2(delta_y, delta_x)
        ls_to_c = Line(self.center, angle)        

        # Useful angles to have
        # theta - angle between norm and line
        # base  - angle of the ls_to_c line
        # phi   - angle between line and ls_to_c line
        theta = norm.angle_between(line)
        base  = ls_to_c.angle
        phi   = ls_to_c.angle_between(line)

        # The angle of the reflection is equal to
        # if phi > 0 then angle = base - ( pi - 2*theta + abs(phi))
        # else            angle = base + ( pi - 2*theta + abs(phi))
        if phi > 0:
            angle = base - ( mp.pi - 2*theta + abs(phi))
        else:
            angle = base + ( mp.pi - 2*theta + abs(phi))

        return Line(intersection_point, angle)

