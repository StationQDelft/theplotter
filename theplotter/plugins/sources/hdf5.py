import h5py
import numpy as np

import theplotter.graph.nodes as nodes

class HDF5Source(nodes.Source):
    def __init__(self, location, key, **kwargs):
        super().__init__(**kwargs)
        self.location = location
        self.key = key

    def run(self):
        f = h5py.File(self.location, 'r')
        self.dataset = np.array(f[self.key])
        f.close()
        self.need_update = False
