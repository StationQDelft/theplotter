import theplotter.graph.nodes as nodes

class SliceTransformation(nodes.Node):
    def __init__(self, datasource, slice_operator):
        super().__init__()
        self.set_sources([datasource])
        self.slice_operator = slice_operator

    def run(self):
        data = self.datasources[0].get_data()
        self.dataset = data[self.slice_operator]

        self.need_update = False

    def update_slice_operator(self, slice_operator):
        self.slice_operator = slice_operator
        self.need_update = True