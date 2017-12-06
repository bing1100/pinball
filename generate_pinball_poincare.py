import pinball as pinball
import poincare as poincare
import mpmath as mp

# Global variables for the cd and cr ratio
CD_CR_RATIO = 2.5
STEP_X = 0.01
STEP_Y = mp.pi / 360
MAX_REFLECTIONS = 2


domain_x = [0, 1]
domain_y  = [-mp.pi/2 , mp.pi/2]

global_intervals = []

def frange (start, stop, incr):

    i = start

    while i <= stop:

        yield i

        i += incr

pinball.set_cd_cr_ratio(CD_CR_RATIO)

for x_val in frange(domain_x[0], domain_x[1], STEP_X):

    interval_x = []
    interval_theta = []

    for theta in frange(domain_y[0], domain_y[1], STEP_Y):

        cline  = pinball.create_line(x_val, theta) 

        res = pinball.run(cline, MAX_REFLECTIONS, False)

        if res[0]:
            interval_x.append(x_val)
            interval_theta.append(theta)

            #print([interval_x, interval_theta])
        else:
            if len(interval_x) != 0:
                global_intervals.append([interval_x, interval_theta])
                interval_x = []
                interval_theta = []

fig = poincare.Poincare(global_intervals)

fig.show_poincare()
        



