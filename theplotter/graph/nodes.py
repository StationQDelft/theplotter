class Node():
    def __init__(self):
        super().__init__()
        self.dataset = None
        self.datasources = []
        self.by_ref = []  # A bool per datasource to signal if the data is by_ref(True) or a copy (False)
        self.datatargets = []

    def run(self):
        '''
        void
        :return: void
        '''
        raise NotImplementedError

    def get_data(self):
        return self.dataset


class Source(Node):
    def __init__(self):
        super().__init__()


class Target(Node):
    def __init__(self):
        super().__init__()




