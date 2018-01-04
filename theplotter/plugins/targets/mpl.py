import numpy as np

from matplotlib import pyplot as plt
import theplotter.graph.nodes as nodes
from matplotlib.widgets import RectangleSelector
from matplotlib.widgets import PolygonSelector
from matplotlib.widgets import Button
import time

import multiprocessing
import threading


class MPLWindow:
    def __init__(self, nrows, ncols):
        super().__init__()
        self.exitflag = False

        self.fig, self.ax = plt.subplots(ncols=ncols,
                                         nrows=nrows, squeeze=False)
        self.viewports = np.array([[MPLViewport(axis, self) for axis in row] for row in self.ax])
        plt.show()
        def update():
            for row in self.viewports:
                for viewport in row:
                    viewport.mplplot.play()
            self.fig.canvas.draw()
        def on_key(event):
            if event.key == ' ':
                update()
        self.fig.canvas.mpl_connect('key_press_event', on_key)

    def __getitem__(self, item):
        return self.viewports[item]

class MPLViewport:
    def __init__(self, ax, mplwindow):
        super().__init__()
        self.ax = ax
        self.mplwindow = mplwindow
        self.mplplot = None

    def set_mplplot(self, mplplot):
        self.mplplot = mplplot


class MPLPlot(nodes.Target):
    def __init__(self, plottarget=None, **kwargs):
        super().__init__(**kwargs)
        self.widgets = {}
        if plottarget is not None:
            self.set_viewport(plottarget)
        else:
            self.viewport = None

    def set_viewport(self, viewport):
        self.viewport = viewport
        self.viewport.set_mplplot(self)
        #self.add_widget('play', Button(self.ax, 'Play'))
        #self.widgets['play'].on_clicked(self.play)

    def add_widget(self, name, widget):
        self.widgets.update({name:widget})

    def add_rectangle_selector(self, callback):
        def onselect(eclick, erelease):
            callback((eclick.xdata, eclick.ydata),(erelease.xdata, erelease.ydata))
        self.add_widget('rectangle_selector', RectangleSelector(self.viewport.ax, onselect, drawtype='box'))

    def add_polygon_selector(self, callback):
        def onselect(event):
            callback(event[0], event[1])
        self.add_widget('polygon_selector', PolygonSelector(self.viewport.ax, onselect))


class MultiMPLTarget(nodes.Target):
    def __init__(self, layout):
        super().__init__()
        self.widgets = {}
        self.layout = layout
        self.fig, self.ax = plt.subplots(ncols=len(layout[0]),
                                         nrows=len(layout), squeeze=False)
        for r, row in enumerate(layout):
            for c, column in enumerate(layout[r]):
                column.set_ax(self.ax[r][c])
                self.add_sources(column.datasources)

    def run(self):
        for r, row in enumerate(self.layout):
            for c, column in enumerate(self.layout[r]):
                column.run()
        self.fig.canvas.draw()

    def add_widget(self, name, widget):
        self.widgets.update({name:widget})



class pcolormesh(MPLPlot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def run(self):
        self.viewport.ax.cla()
        self.viewport.ax.pcolormesh(self.datasources[0].get_data(),
                           self.datasources[1].get_data(),
                           self.datasources[2].get_data())

class lineplot(MPLPlot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def run(self):
        self.viewport.ax.cla()
        self.viewport.ax.plot(self.datasources[0].get_data(),
                     self.datasources[1].get_data())