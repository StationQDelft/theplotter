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

    def from_polygon(self, points):
        #print(points)
        self.base = np.array([points[0][0], points[0][1]])
        self.xvec = np.array([points[1][0]-points[0][0], points[1][1]-points[0][1]])
        yvec_t = np.array([points[2][0]-points[1][0], points[2][1]-points[1][1]])
        self.yvec = yvec_t - (self.xvec * np.dot(self.xvec, yvec_t)/np.dot(self.xvec, self.xvec))
        self.need_update = True


    def connect_plot(self, plot):
        plot.add_polygon_selector(self.from_polygon)

    def run(self):
        dt = np.dtype([('x', np.float64), ('y', np.float64)])
        self.dataset = np.array([[tuple(self.base + i * self.xvec + j * self.yvec)
                                 for i in np.linspace(0, 1, self.xpoints)]
                                 for j in np.linspace(-0.5, 0.5, self.ypoints)
                                 ], dtype=dt)
        self.need_update = False

class from_array(nodes.Source):
    def __init__(self, array, **kwargs):
        super().__init__(**kwargs)
        self.dataset = array
        self.need_update=False
