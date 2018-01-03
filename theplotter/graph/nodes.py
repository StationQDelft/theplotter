class Node():
    def __init__(self):
        super().__init__()
        self.dataset = None
        self.datasources = []
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

    def add_target_if_absent(self, target):
        if target not in self.datatargets:
            self.datatargets.append(target)


class Source(Node):
    def __init__(self):
        super().__init__()


class Target(Node):
    def __init__(self):
        super().__init__()




