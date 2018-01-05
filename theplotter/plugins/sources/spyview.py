import numpy as np

from fusion.legacy.spyview_format import SpyViewFormat

import theplotter.graph.nodes as nodes


class SpyviewSource(nodes.Source):
    def __init__(self, location, **kwargs):
        super().__init__(**kwargs)
        self.location = location

    def run(self):
        spyviewformat = SpyViewFormat()
        with open(self.location) as f:
            header = spyviewformat._read_header(f, '#')
        dt_list = []
        column_list = []
        shape_list = []
        for name, info in header[1].items():
            if name.startswith('Column '):
                column_list.append([int(name[7:]), name, info])
        for index, name, info in sorted(column_list, key=lambda column: column[0]):
            dt_list.append((name, np.float64))
            if info['type'] == 'coordinate':
                shape_list.append(int(info['size']))
        shape = tuple(shape_list)
        self.dataset = np.loadtxt(self.location, dtype=np.dtype(dt_list)).reshape(shape, order='F').transpose()

        self.need_update = False
