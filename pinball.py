import computation as cpt
import matplotlib.pyplot as mpp
import mpmath as mp
'''
 
 Global variables

'''

# Global Variables to change
# The total number of relfections we want to keep track of
MAX_REFLECTIONS = 2
# The ratio of distance between circle centers and radius of circle         
CD_CR_RATIO     = 2.5
# The angle of the first line from c1
START_ANGLE     = mp.pi/5

# Other global variables
fig = mpp.gca()     
numReflections = 0  
hasEscaped = False 
sourceCircle = 1
cLine = cpt.Line((0,0), START_ANGLE)
cxPoint = mp.sqrt(CD_CR_RATIO ** 2 - (CD_CR_RATIO/2) **2 )
c1Cen = [0,0]
c2Cen = [cxPoint, CD_CR_RATIO/2]
c3Cen = [cxPoint, -CD_CR_RATIO/2]
c1 = cpt.Circle(c1Cen, 1)
c2 = cpt.Circle(c2Cen, 1)
c3 = cpt.Circle(c3Cen, 1)
all_circles = [c1.eq, c2.eq,c3.eq]

'''

Functions 

'''
# Helper function to display graphs and circles
def show_shapes(patchs):

    for patch in patchs:
        fig.add_patch(patch)
    mpp.axis('scaled')
    mpp.title('Pinball trajectory')
    mpp.grid(True)
    mpp.show()

# Helper reflection stepper that does work for each possible reflection
def reflectionStepper(c1_data, c2_data, c3_data):

    global cLine, sourceCircle, hasEscaped

    if c1_data[0]: # intersection exists with c1

        # Set the x and y coords to plot
        x_line = [cLine.point[0], c1_data[2][0]]
        y_line = [cLine.point[1], c1_data[2][1]]

        # Plot norm and the current line
        fig.plot(c1_data[3].eq[0], c1_data[3].eq[1], linestyle = ':')
        fig.plot(x_line, y_line)

        # Set globals for next iteration
        sourceCircle = 1
        cLine = c1_data[1]

        
    elif c2_data[0]: # intersection exists with c2

        # Set the x and y coords to plot
        x_line = [cLine.point[0], c2_data[2][0]]
        y_line = [cLine.point[1], c2_data[2][1]]

        # Plot norm and the current line
        fig.plot(c2_data[3].eq[0], c2_data[3].eq[1], linestyle = ':')
        fig.plot(x_line, y_line)

        # Set globals for the next iteration
        sourceCircle = 2
        cLine = c2_data[1]

    elif c3_data[0]: # intersection exists with c3

        # Set the x and y coords to plot
        x_line = [cLine.point[0], c3_data[2][0]]
        y_line = [cLine.point[1], c3_data[2][1]]

        # Plot norm and the current line
        fig.plot(c3_data[3].eq[0], c3_data[3].eq[1], linestyle = ':')
        fig.plot(x_line, y_line)

        # Set globals for the next iteration
        sourceCircle = 3
        cLine = c3_data[1]

    else: # no intersection with any circle

        # Plot the cline
        fig.plot(cLine.eq[0], cLine.eq[1])

        # Set the global variable hasEscaped to True
        hasEscaped = True

'''

Script

'''

# Find the next reflection as long as total number of reflection
#  smaller than a max number and the line has not escaped
while ( numReflections <= MAX_REFLECTIONS and not hasEscaped):
    
    # Increment the number of reflections so far
    numReflections += 1

    if sourceCircle == 1: # The cline reflected from c1

        # Set the data and call the stepper
        c1_data = [False] # cline can't reflect on c1 if from c1
        c2_data = c2.reflection(cLine)
        c3_data = c3.reflection(cLine)

        reflectionStepper(c1_data, c2_data, c3_data)

    elif sourceCircle == 2: # The cline reflected from c2
        
        # Set the data and call the stepper
        c1_data = c1.reflection(cLine)
        c2_data = [False] # cline can't reflect on c2 if from c2
        c3_data = c3.reflection(cLine)
        
        reflectionStepper(c1_data, c2_data, c3_data)

    elif sourceCircle == 3:

        # Set the data and call the stepper
        c1_data = c1.reflection(cLine)
        c2_data = c2.reflection(cLine)
        c3_data = [False] # cline can't reflect on c3 if from c3

        reflectionStepper(c1_data, c2_data, c3_data)

# Plot all circles and lines
show_shapes(all_circles)
    