import computation as cpt
import matplotlib.pyplot as mpp
import mpmath as mp

# Global variables

MAX_REFLECTIONS = 2
CD_CR_RATIO = 3
START_ANGLE = mp.pi/2

fig = mpp.gca()

numReflections = 0
hasEscaped = False
whichCircle = 1
cLine = cpt.Line((0,0), START_ANGLE)

cxPoint = mp.sqrt(CD_CR_RATIO ** 2 - (CD_CR_RATIO/2) **2 )

c1Cen = [0,0]
c2Cen = [cxPoint, CD_CR_RATIO/2]
c3Cen = [cxPoint, -CD_CR_RATIO/2]

c1 = cpt.Circle(c1Cen, 1)
c2 = cpt.Circle(c2Cen, 1)
c3 = cpt.Circle(c3Cen, 1)

all_circles = [mpp.Circle(c1Cen,1), mpp.Circle(c2Cen,1),mpp.Circle(c3Cen,1)]

def show_shapes(patchs):

    for patch in patchs:
        fig.add_patch(patch)
    mpp.axis('scaled')
    mpp.grid(True)
    mpp.show()

# Start of script

def reflectionStepper(c1_data, c2_data, c3_data, line):

    global cLine, whichCircle, hasEscaped

    start_x = line.point[0]
    start_y = line.point[1]

    if c1_data[0]:
        whichCircle = 1
        cLine = cpt.Line(c1_data[1], c1_data[2])
    elif c2_data[0]:
        whichCircle = 2
        cLine = cpt.Line(c2_data[1], c2_data[2])
    elif c3_data[0]:
        whichCircle = 3
        cLine = cpt.Line(c3_data[1], c3_data[2])
    else:
        hasEscaped = True
        whichCircle = 0
        cLine = cpt.Line(line.newPoint, 0)

    line_x = [start_x, cLine.point[0]]
    line_y = [start_y, cLine.point[1]]

    return [line_x, line_y]

while ( numReflections < MAX_REFLECTIONS and not hasEscaped):
    
    numReflections += 1

    if whichCircle == 1:

        c1_data = [False]
        c2_data = c2.reflection(cLine)
        c3_data = c3.reflection(cLine)

        line_data = reflectionStepper(c1_data, c2_data, c3_data, cLine)

        fig.plot(line_data[0], line_data[1])

    elif whichCircle == 2:

        c1_data = c1.reflection(cLine)
        c2_data = [False]
        c3_data = c3.reflection(cLine)

        line_data = reflectionStepper(c1_data, c2_data, c3_data, cLine)

        fig.plot(line_data[0], line_data[1])

    elif whichCircle == 3:

        c1_data = c1.reflection(cLine)
        c2_data = c2.reflection(cLine)
        c3_data = [False]

        line_data = reflectionStepper(c1_data, c2_data, c3_data, cLine)

        fig.plot(line_data[0], line_data[1])

show_shapes(all_circles)




        



    