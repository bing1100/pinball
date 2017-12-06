import matplotlib.pyplot as plt

class Poincare():

    def __init__(self, intervals):

        self.intervals = intervals
        self.fig       = plt.gca()

    def add_interval(self,interval):

        self.intervals.append(interval)

    def show_poincare(self):

        for interval in self.intervals:

            self.fig.plot(interval[0], interval[1])

        plt.axis('scaled')
        plt.title('Poincare Section')
        plt.grid(True)
        plt.show()



