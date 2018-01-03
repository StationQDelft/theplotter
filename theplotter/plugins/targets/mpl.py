from matplotlib import pyplot as plt
import theplotter.graph.nodes as nodes

class MultiMPLTarget(nodes.Target):
    def __unit__(self):
        super().__init__()


class pcolormesh(nodes.Target):
    def __init__(self):
        super().__init__()

    def run(self):
        plt.pcolormesh(self.datasources[0].get_data(),
                       self.datasources[1].get_data(),
                       self.datasources[2].get_data())
        plt.show()