import numpy as np
import theplotter.graph.nodes as nodes

class create_orthogonal_grid(nodes.Source):
    def __init__(self, xpoints, ypoints, **kwargs):
        super().__init__(**kwargs)
        self.xpoints = xpoints
        self.ypoints = ypoints
        self.xvec = None
        self.yvec = None
        self.base = None

    def from_polygon(self, xlist, ylist):
        self.base = [xlist[0], ylist[0]]
        self.xvec = [xlist[1]-xlist[0], ylist[1]-ylist[0]]
        self.yvec = [xlist[2]-xlist[0], ylist[2]-ylist[0]]
        self.yvec = self.yvec - self.xvec * np.dot(self.xvec, self.yvec)
        self.need_update = True


    def connect_plot(self, plot):
        plot.add_polygon_selector(self.from_polygon)

    def run(self):
        self.dataset = np.array([self.base + i * self.xvec + j * self.yvec for i in np.linspace(0, 1, x_res) for j in np.linspace(-0.5, 0.5, y_res)])
        self.need_update = False
