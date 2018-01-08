import numpy as np

class Node():
    def __init__(self, datasources=None):
        super().__init__()
        self.dataset = None
        if datasources is None:
            self.datasources = []
        else:
            self.set_sources(datasources)
        self.by_ref = []  # A bool per datasource to signal if the data is by_ref(True) or a copy (False)
        self.datatargets = []

        self.need_update = True

    def run(self):
        '''
        void
        :return: void
        '''
        raise NotImplementedError

    def play(self):
        for source in self.datasources:
            source.play()
        if self.need_update:
            #print('run on ', self)
            self.run()
            for target in self.datatargets:
                target.need_update = True

    def get_data(self):
        return self.dataset

    def set_sources(self, sources):
        self.datasources = sources
        for source in self.datasources:
            source.add_target_if_absent(self)

    def add_sources(self, sources):
        for source in sources:
            self.datasources.append(source)
            source.add_target_if_absent(self)

    def add_target_if_absent(self, target):
        if target not in self.datatargets:
            self.datatargets.append(target)

    def __getitem__(self, item):
        return SliceTransformation(self, item)

    def __add__(self, other):
        return AddTransformation(datasources=[self, other])


class Source(Node):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Target(Node):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class SliceTransformation(Node):
    def __init__(self, datasource, slice_operator, **kwargs):
        super().__init__(**kwargs)
        self.set_sources([datasource])
        self.slice_operator = slice_operator

    def run(self):
        data = self.datasources[0].get_data()
        self.dataset = data[self.slice_operator]

        self.need_update = False

    def update_slice_operator(self, slice_operator):
        self.slice_operator = slice_operator
        self.need_update = True

class AddTransformation(Node):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def run(self):
        ds1 = self.datasources[0].get_data()
        ds2 = self.datasources[1].get_data()
        if ds1.dtype != ds2.dtype:
            raise Exception("datasets have unequal dtype")
        if ds1.shape != ds2.shape:
            raise Exception("Datasets have unequal shape")
        if len(ds1.dtype)==0:
            self.dataset = ds1 + ds2
        else:
            self.dataset = np.zeros(ds1.shape, dtype=ds1.dtype)
            for field in ds1.dtype.names:
                self.dataset[field] = ds1[field] + ds2[field]




