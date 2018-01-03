import numpy as np

from fusion.legacy.spyview_format import SpyViewFormat

import graph.nodes as nodes


class SpyviewSource(nodes.Source):
    def __init__(self, location):
        super().__init__()
        self.location = location

    def run(self):
        spyviewformat = SpyViewFormat()
        with open(self.location) as f:
            header = spyviewformat._read_header(f, '#')
        dt_list = []
        shape_list = []
        for name, info in header[1].items():
            if name.startswith('Column '):
                dt_list.append((name, np.float64))
                if info['type'] == 'coordinate':
                    shape_list.append([int(name[7:]),int(info['size'])])
        shape = tuple([item[1] for item in sorted(shape_list, key=lambda column: column[0])])
        data = np.loadtxt(self.location, dtype=np.dtype(dt_list)).reshape(shape, order='F')
