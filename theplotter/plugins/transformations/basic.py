import numpy as np

import theplotter.graph.nodes as nodes
import scipy.interpolate as interpolate


class Crop2D(nodes.Node):
    def __init__(self, xcolumn, ycolumn, xcolumn_name, ycolumn_name, **kwargs):
        super().__init__(**kwargs)
        self.xcolumn = xcolumn
        self.ycolumn = ycolumn
        self.xcolumn_name = xcolumn_name
        self.ycolumn_name = ycolumn_name
        self.pos_1 = None
        self.pos_2 = None

    def set_cropbox(self, pos_1, pos_2):
        self.pos_1 = pos_1
        self.pos_2 = pos_2
        self.need_update = True

    def connect_plot(self, plot):
        plot.add_rectangle_selector(self.set_cropbox)

    def run(self):
        data = self.datasources[0].get_data()
        s = [0 for c in data.shape]
        s[self.xcolumn] = slice(None)
        axis = data[tuple(s)]
        b = np.logical_and(self.pos_1[0] < axis[self.xcolumn_name], axis[self.xcolumn_name] < self.pos_2[0])

        s = [slice(None) for c in data.shape]
        s[self.xcolumn] = b
        self.dataset = data[tuple(s)]

        s = [0 for c in data.shape]
        s[self.ycolumn] = slice(None)
        axis = data[tuple(s)]
        b = np.logical_and(self.pos_1[1] < axis[self.ycolumn_name], axis[self.ycolumn_name] < self.pos_2[1])

        s = [slice(None) for c in data.shape]
        s[self.ycolumn] = b
        self.dataset = self.dataset[tuple(s)]

        self.need_update = False


class Average(nodes.Node):
    def __init__(self, axis, **kwargs):
        super().__init__(**kwargs)
        self.axis = axis

    def run(self):
        data = self.datasources[0].get_data()
        self.dataset = np.average(data, axis=self.axis)

        self.need_update = False


class Interpolate(nodes.Node):
    def __init__(self, method='linear', **kwargs):
        super().__init__(**kwargs)
        self.method = method

    def run(self):
        orig_grid = self.datasources[0].get_data()
        orig_values = self.datasources[1].get_data()
        new_grid = self.datasources[2].get_data()
        self.dataset = interpolate.griddata(orig_grid, orig_values, new_grid, method=self.method)
        self.need_update = False