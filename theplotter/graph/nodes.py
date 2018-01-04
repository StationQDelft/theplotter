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
            print('run on ', self)
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




